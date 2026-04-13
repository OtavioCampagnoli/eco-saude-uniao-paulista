from __future__ import annotations

from app.domain.models import Inspection, ItemStatus


def generate_recommendations(inspection: Inspection) -> list[str]:
    recs: list[str] = []

    critical_items = [i for i in inspection.items if i.status == ItemStatus.CRITICAL]
    attention_items = [i for i in inspection.items if i.status == ItemStatus.ATTENTION]

    def has_text(items, text: str) -> bool:
        t = text.lower()
        return any(t in i.name.lower() for i in items)

    if has_text(critical_items, "vazamento"):
        recs.append("Realizar manutenção imediata: há indício de vazamento crítico.")

    if has_text(critical_items + attention_items, "sem sabonete"):
        recs.append("Repor sabonete e reforçar orientação de higiene das mãos.")

    if has_text(critical_items + attention_items, "bebedouro sujo"):
        recs.append("Realizar limpeza do bebedouro e definir rotina de higienização.")

    if not recs and critical_items:
        recs.append("Priorizar correção dos itens críticos identificados na inspeção.")

    if not recs and attention_items:
        recs.append("Planejar correções para itens de atenção e reforçar conscientização.")

    if not recs:
        recs.append("Manter rotina de verificação preventiva (inspeção periódica).")

    return recs