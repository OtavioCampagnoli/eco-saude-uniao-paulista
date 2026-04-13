from __future__ import annotations

import streamlit as st

from app.infra.storage_csv import CsvInspectionRepository
from app.services.inspection_service import InspectionService
from app.ui.pages import render_dashboard, render_export, render_new_inspection


def build_service() -> InspectionService:
    repo = CsvInspectionRepository(csv_path="data/inspections.csv")
    return InspectionService(repo=repo)


def main() -> None:
    st.set_page_config(page_title="EcoSaúde UP", layout="wide")

    st.title("EcoSaúde UP — Checklist & Dashboard")
    st.caption("Projeto de Extensão — Meio Ambiente e Saúde (ODS 6 / ODS 3)")

    service = build_service()

    page = st.sidebar.radio(
        "Navegação",
        options=["Nova inspeção", "Dashboard", "Exportar"],
        index=0,
    )

    if page == "Nova inspeção":
        render_new_inspection(service)
    elif page == "Dashboard":
        render_dashboard(service)
    else:
        render_export(service)

    st.divider()
    st.caption("Projeto desenvolvido por Otávio Campagnoli.")


if __name__ == "__main__":
    main()