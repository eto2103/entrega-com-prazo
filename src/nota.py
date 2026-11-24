def calcular_nota_final(nota, prazo, entrega, justificativa_aprovada, novo_prazo):
    """Calcula a nota final considerando atraso e eventual novo prazo aprovado."""
    prazo_efetivo = prazo
    if justificativa_aprovada and novo_prazo is not None:
        prazo_efetivo = novo_prazo

    atraso = entrega - prazo_efetivo
    if atraso.total_seconds() <= 0:
        dias_atraso = 0
    else:
        dias_atraso = atraso.days + bool(atraso.seconds or atraso.microseconds)

    desconto_percentual = min(dias_atraso * 10, 50)
    if dias_atraso > 5:
        return {
            "aceita": False,
            "nota_final": None,
            "desconto_percentual": desconto_percentual,
            "dias_atraso": dias_atraso,
        }

    nota_final = nota * (1 - desconto_percentual / 100)
    return {
        "aceita": True,
        "nota_final": nota_final,
        "desconto_percentual": desconto_percentual,
        "dias_atraso": dias_atraso,
    }
