# RF-001
# Dado nota 10 e prazo 10/11/2026 23:59
# Quando a entrega e feita exatamente em 10/11/2026 23:59
# Entao aceita e verdadeiro, nota_final e 10.00, desconto_percentual e 0 e dias_atraso e 0

# RF-002
# Dado nota 10 e prazo 10/11/2026 23:59
# Quando a entrega e feita em 13/11/2026 00:59 (2 dias e 1 hora de atraso)
# Entao dias_atraso e 3, desconto_percentual e 30 e nota_final e 7.00

# RF-003
# Dado nota 10 e prazo 10/11/2026 23:59
# Quando a entrega e feita em 15/11/2026 23:59 (exatamente 5 dias de atraso)
# Entao aceita e verdadeiro, desconto_percentual e 50 e nota_final e 5.00

# RF-004
# Dado nota 10 e prazo 10/11/2026 23:59
# Quando a entrega e feita em 16/11/2026 00:00 (5 dias e 1 minuto de atraso)
# Entao aceita e falso e nota_final e None

# RF-005
# Dado nota 10, justificativa aprovada e novo prazo 15/11/2026 23:59
# Quando a entrega e feita em 14/11/2026 10:00
# Entao aceita e verdadeiro, desconto_percentual e 0 e nota_final e 10.00

from datetime import datetime, timezone

from src.nota import calcular_nota_final


TZ = timezone.utc


def test_entrega_exatamente_no_prazo():
    prazo = datetime(2026, 11, 10, 23, 59, tzinfo=TZ)

    resultado = calcular_nota_final(10, prazo, prazo, False, None)

    assert resultado["aceita"] is True
    assert resultado["nota_final"] == 10
    assert resultado["desconto_percentual"] == 0
    assert resultado["dias_atraso"] == 0


def test_entrega_atrasada_perde_dez_porcento_por_dia_iniciado():
    prazo = datetime(2026, 11, 10, 23, 59, tzinfo=TZ)
    entrega = datetime(2026, 11, 13, 0, 59, tzinfo=TZ)

    resultado = calcular_nota_final(10, prazo, entrega, False, None)

    assert resultado["dias_atraso"] == 3
    assert resultado["desconto_percentual"] == 30
    assert resultado["nota_final"] == 7


def test_desconto_nao_passa_de_cinquenta_porcento():
    prazo = datetime(2026, 11, 10, 23, 59, tzinfo=TZ)
    entrega = datetime(2026, 11, 15, 23, 59, tzinfo=TZ)

    resultado = calcular_nota_final(10, prazo, entrega, False, None)

    assert resultado["aceita"] is True
    assert resultado["desconto_percentual"] == 50
    assert resultado["nota_final"] == 5


def test_entrega_mais_de_cinco_dias_atrasada_e_recusada():
    prazo = datetime(2026, 11, 10, 23, 59, tzinfo=TZ)
    entrega = datetime(2026, 11, 16, 0, 0, tzinfo=TZ)

    resultado = calcular_nota_final(10, prazo, entrega, False, None)

    assert resultado["aceita"] is False
    assert resultado["nota_final"] is None


def test_justificativa_aprovada_elimina_desconto_dentro_do_novo_prazo():
    prazo = datetime(2026, 11, 10, 23, 59, tzinfo=TZ)
    novo_prazo = datetime(2026, 11, 15, 23, 59, tzinfo=TZ)
    entrega = datetime(2026, 11, 14, 10, 0, tzinfo=TZ)

    resultado = calcular_nota_final(
        10,
        prazo,
        entrega,
        True,
        novo_prazo,
    )

    assert resultado["aceita"] is True
    assert resultado["desconto_percentual"] == 0
    assert resultado["nota_final"] == 10
