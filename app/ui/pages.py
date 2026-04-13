from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app.domain.models import Inspection, InspectionItem, ItemStatus
from app.domain.scoring import score_inspection
from app.services.inspection_service import InspectionService


DEFAULT_ITEMS = [
    "Vazamento em torneiras",
    "Sem sabonete",
    "Sem papel para secar as mãos",
    "Bebedouro sujo",
    "Sinalização de economia de água ausente",
]


def render_new_inspection(service: InspectionService) -> None:
    st.subheader("Nova inspeção")

    with st.form("inspection_form"):
        sector = st.text_input("Setor (ex.: Banheiros, Bebedouros, Pátio)", value="Banheiros")
        notes = st.text_area("Observações gerais (opcional)")

        st.markdown("### Checklist")
        items: list[InspectionItem] = []
        for name in DEFAULT_ITEMS:
            cols = st.columns([3, 2, 3])
            with cols[0]:
                st.write(name)
            with cols[1]:
                status = st.selectbox(
                    "Status",
                    options=[ItemStatus.OK, ItemStatus.ATTENTION, ItemStatus.CRITICAL],
                    format_func=lambda x: x.value,
                    key=f"status_{name}",
                )
            with cols[2]:
                comment = st.text_input("Comentário (opcional)", key=f"comment_{name}")

            items.append(InspectionItem(name=name, status=status, comment=comment or None))

        submitted = st.form_submit_button("Salvar inspeção")

    if submitted:
        inspection = Inspection(sector=sector, items=items, notes=notes or None)
        service.create_inspection(inspection)

        st.success("Inspeção salva com sucesso.")
        st.write(f"Score desta inspeção: **{score_inspection(inspection)} / 100**")

        recs = service.get_recommendations_for(inspection)
        st.markdown("### Recomendações")
        for r in recs:
            st.write(f"- {r}")


def render_dashboard(service: InspectionService) -> None:
    st.subheader("Dashboard")

    inspections = service.list_inspections()
    if not inspections:
        st.info("Ainda não há inspeções registradas. Vá em 'Nova inspeção' para começar.")
        return

    metrics = service.get_dashboard_metrics()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total de inspeções", metrics.total_inspections)
    c2.metric("Setores avaliados", len(metrics.score_by_sector))
    c3.metric("Itens críticos", metrics.issues_by_status.get(ItemStatus.CRITICAL.value, 0))

    st.markdown("### Score por setor")
    df_sector = pd.DataFrame(
        [{"Setor": k, "Score (0–100)": v} for k, v in metrics.score_by_sector.items()]
    )
    fig_sector = px.bar(df_sector, x="Setor", y="Score (0–100)", range_y=[0, 100])
    st.plotly_chart(fig_sector, use_container_width=True)

    st.markdown("### Itens por severidade")
    df_issues = pd.DataFrame(
        [{"Status": k, "Quantidade": v} for k, v in metrics.issues_by_status.items()]
    )
    fig_issues = px.pie(df_issues, names="Status", values="Quantidade")
    st.plotly_chart(fig_issues, use_container_width=True)

    if metrics.top_problem_items:
        st.markdown("### Top itens problemáticos (ATENÇÃO/CRÍTICO)")
        df_top = pd.DataFrame(metrics.top_problem_items, columns=["Item", "Ocorrências"])
        st.dataframe(df_top, use_container_width=True)


def render_export(service: InspectionService) -> None:
    st.subheader("Exportar")

    inspections = service.list_inspections()
    if not inspections:
        st.info("Sem dados para exportar.")
        return

    rows = []
    for ins in inspections:
        for item in ins.items:
            rows.append(
                {
                    "id": str(ins.id),
                    "created_at": ins.created_at.isoformat(),
                    "school_name": ins.school_name,
                    "sector": ins.sector,
                    "notes": ins.notes or "",
                    "item_name": item.name,
                    "item_status": item.status.value,
                    "item_comment": item.comment or "",
                }
            )

    df = pd.DataFrame(rows)
    csv_bytes = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Baixar CSV (inspeções + itens)",
        data=csv_bytes,
        file_name="ecosaupe_export.csv",
        mime="text/csv",
    )