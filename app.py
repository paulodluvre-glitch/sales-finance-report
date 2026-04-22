from __future__ import annotations

import base64
import io
import json
import re
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# =========================
# Configuração Base
# =========================

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo-clivet.jpg"
PARTNER_LOGO_PATH = BASE_DIR / "logo-mauricio.png"
FINANCE_MAP_FILE = BASE_DIR / "mapeamento_financeiro.json"

CLIENT_NAME = "CliVet Clínica Veterinária Taquari"
CLIENT_CNPJ = "36.780.147/0001-99"
PARTNER_NAME = "MLG Contabilidade e Finanças"
PARTNER_WHATSAPP = "61 99138 0108"
PARTNER_EMAIL = "mauricio@morellicontabil.com"
PARTNER_CNPJ = "27.252.772/0001-77"

DAY_ORDER = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]

PERIOD_PRESETS = {
    "Dia": 0,
    "Semana": 6,
    "Mês": 29,
    "3 Meses": 89,
    "6 Meses": 179,
    "1 Ano": 364,
}

DAY_NAME_PT = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}

UPLOAD_TYPES = ["csv", "xlsx", "xls"]


# =========================
# Estilo e Identidade
# =========================

def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --blue-950: #1f3a6d;
            --blue-900: #2f4f8f;
            --blue-700: #5e7fc1;
            --blue-500: #89a7e0;
            --blue-200: #dbe6ff;
            --blue-100: #eef4ff;
            --ink: #1f2d44;
            --muted: #6b7a90;
            --card: #ffffff;
            --border: #dce6f7;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(137, 167, 224, 0.16), transparent 28%),
                radial-gradient(circle at top right, rgba(94, 127, 193, 0.12), transparent 26%),
                linear-gradient(180deg, #f7faff 0%, #ffffff 48%, #f5f8ff 100%);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f3f7ff 0%, #ffffff 100%);
            border-right: 1px solid var(--border);
        }

        .hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, rgba(31, 58, 109, 0.97), rgba(94, 127, 193, 0.92));
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 26px;
            padding: 1.2rem 1.2rem 1rem 1.2rem;
            box-shadow: 0 18px 36px rgba(31, 58, 109, 0.16);
            margin-bottom: 1rem;
        }

        .hero::before,
        .hero::after {
            content: "🐾";
            position: absolute;
            font-size: 84px;
            opacity: 0.08;
            color: #ffffff;
            z-index: 0;
            transform: rotate(-10deg);
        }

        .hero::before {
            right: 32px;
            top: -10px;
        }

        .hero::after {
            right: 110px;
            top: 48px;
            transform: rotate(14deg);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 140px 1fr 220px;
            gap: 1rem;
            align-items: center;
            position: relative;
            z-index: 1;
        }

        .hero-logo {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .hero-logo img {
            width: 132px;
            height: auto;
            border-radius: 18px;
            box-shadow: 0 10px 22px rgba(0, 0, 0, 0.10);
        }

        .hero-copy .eyebrow {
            color: rgba(255, 255, 255, 0.84);
            font-size: 0.78rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
            font-weight: 700;
        }

        .hero-copy h1 {
            margin: 0;
            color: #ffffff;
            font-size: 1.8rem;
            line-height: 1.1;
            font-weight: 800;
        }

        .hero-copy p {
            margin: 0.65rem 0 0 0;
            color: rgba(255, 255, 255, 0.90);
            font-size: 0.98rem;
            max-width: 58rem;
        }

        .hero-meta {
            align-self: stretch;
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            color: #ffffff;
        }

        .hero-meta .label {
            font-size: 0.76rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            opacity: 0.86;
            margin-bottom: 0.25rem;
        }

        .hero-meta .value {
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.25;
        }

        .hero-meta .sub {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            opacity: 0.9;
        }

        .section-title {
            color: var(--blue-950);
            font-weight: 800;
            font-size: 1.15rem;
            margin: 0.15rem 0 0.25rem 0;
        }

        .section-note {
            color: var(--muted);
            font-size: 0.92rem;
            margin-bottom: 0.6rem;
        }

        .soft-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1rem 0.7rem 1rem;
            box-shadow: 0 12px 30px rgba(58, 88, 149, 0.08);
        }

        .footer-box {
            background: linear-gradient(180deg, #ffffff 0%, #f7faff 100%);
            border: 1px dashed rgba(94, 127, 193, 0.35);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-top: 1rem;
            color: var(--muted);
        }

        .footer-grid {
            display: grid;
            grid-template-columns: 180px 1fr;
            gap: 1rem;
            align-items: center;
        }

        .footer-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 0.85rem;
        }

        .footer-logo img {
            max-width: 100%;
            height: auto;
        }

        .footer-title {
            color: var(--blue-950);
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .footer-contact {
            margin-top: 0.45rem;
            line-height: 1.65;
        }

        .export-note {
            color: var(--muted);
            font-size: 0.86rem;
            margin-top: 0.2rem;
        }

        .footer-box strong {
            color: var(--blue-950);
        }

        @page {
            size: A4 landscape;
            margin: 8mm;
        }

        @media print {
            [data-testid="stSidebar"],
            header,
            footer,
            .stButton,
            .export-note,
            [data-testid="stFileUploader"] {
                display: none !important;
            }

            [data-baseweb="tab-list"] {
                display: none !important;
            }

            .stApp {
                zoom: 85%;
            }

            .hero,
            .soft-card,
            .footer-box,
            .stPlotlyChart,
            [data-testid="stDataFrame"],
            [data-testid="stMetric"],
            [data-testid="column"] {
                box-shadow: none !important;
                break-inside: avoid !important;
                page-break-inside: avoid !important;
            }

            h1, h2, h3, h4, h5, h6,
            .section-title,
            .section-note,
            .stMarkdown,
            [data-testid="stExpander"] {
                break-inside: avoid !important;
                page-break-inside: avoid !important;
            }

            .stPlotlyChart {
                margin-bottom: 8px !important;
            }

            .footer-grid {
                grid-template-columns: 160px 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def logo_html() -> str:
    if not LOGO_PATH.exists():
        return "<div style='color:white;font-weight:800;'>CliVet</div>"
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
    return f"<img src='data:image/jpeg;base64,{encoded}' alt='CliVet logo' />"


def partner_logo_html() -> str:
    if not PARTNER_LOGO_PATH.exists():
        return f"<div style='color:#1f3a6d;font-weight:800;'>{PARTNER_NAME}</div>"
    encoded = base64.b64encode(PARTNER_LOGO_PATH.read_bytes()).decode("utf-8")
    suffix = PARTNER_LOGO_PATH.suffix.lower().replace(".", "")
    mime = "png" if suffix == "png" else "jpeg"
    return f"<img src='data:image/{mime};base64,{encoded}' alt='{PARTNER_NAME}' />"


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-grid">
            <div class="hero-logo">{logo_html()}</div>
            <div class="hero-copy">
              <div class="eyebrow">Relatório gerencial clínico</div>
              <h1>{CLIENT_NAME}</h1>
              <p>
                Financeiro e comercial tratados de forma independente, com foco em realizado,
                leitura limpa, segurança de dados e exportação pronta para apresentação mensal.
              </p>
            </div>
            <div class="hero-meta">
              <div class="label">CNPJ</div>
              <div class="value">{CLIENT_CNPJ}</div>
              <div class="sub">Dados sensíveis removidos da visualização pública.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_money(value) -> float:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0.0
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "-"}:
        return 0.0
    negative = text.startswith("(") and text.endswith(")")
    text = text.replace("R$", "").replace(" ", "")
    text = re.sub(r"[^\d,.-]", "", text)
    text = text.replace(".", "").replace(",", ".")
    try:
        amount = float(text)
    except ValueError:
        return 0.0
    return -amount if negative else amount


def abbreviate_name(value: str) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if not text:
        return ""
    parts = text.split(" ")
    return " ".join(parts[:2]).title()


def first_non_empty(series: pd.Series) -> str:
    for value in series:
        if pd.notna(value) and str(value).strip():
            return str(value).strip()
    return ""


def join_unique(series: pd.Series) -> str:
    values = []
    for value in series:
        text = str(value).strip()
        if text and text.lower() != "nan":
            values.append(text)
    if not values:
        return ""
    return ", ".join(sorted(set(values)))


def read_uploaded_table(uploaded_file) -> pd.DataFrame:
    raw = uploaded_file.getvalue()
    filename = uploaded_file.name.lower()

    if filename.endswith((".xls", ".xlsx")):
        try:
            return pd.read_excel(io.BytesIO(raw), dtype=str)
        except ImportError as exc:
            raise ValueError(
                "Não foi possível ler a planilha Excel. Verifique se as dependências do projeto foram instaladas por completo."
            ) from exc
        except Exception as exc:
            raise ValueError("Não foi possível ler a planilha Excel enviada.") from exc

    for encoding in ("utf-8-sig", "latin1", "cp1252"):
        try:
            return pd.read_csv(
                io.BytesIO(raw),
                sep=";",
                dtype=str,
                keep_default_na=False,
                encoding=encoding,
                engine="python",
            )
        except Exception:
            continue

    for encoding in ("utf-8-sig", "latin1", "cp1252"):
        try:
            return pd.read_csv(
                io.BytesIO(raw),
                sep=",",
                dtype=str,
                keep_default_na=False,
                encoding=encoding,
                engine="python",
            )
        except Exception:
            continue

    raise ValueError("Não foi possível ler o arquivo enviado.")


def detect_dataset_kind(df: pd.DataFrame) -> str:
    cols = {str(col).strip() for col in df.columns}
    finance_keys = {"Data", "Conta", "Categoria", "Receita", "Despesa", "Valor pago", "Natureza"}
    sales_keys = {
        "Data e hora",
        "Venda",
        "Status da venda",
        "Cliente",
        "Animal",
        "Espécie",
        "Raça",
        "Tipo do Item",
        "Grupo",
        "Produto/serviço",
        "Líquido",
    }

    finance_hits = len(cols & finance_keys)
    sales_hits = len(cols & sales_keys)

    if finance_hits >= 5 and finance_hits > sales_hits:
        return "financeiro"
    if sales_hits >= 7 and sales_hits > finance_hits:
        return "comercial"
    return "desconhecido"


def columns_preview(df: pd.DataFrame, limit: int = 10) -> str:
    cols = [str(col).strip() for col in df.columns if str(col).strip()]
    if not cols:
        return "nenhuma coluna identificada"
    preview = ", ".join(cols[:limit])
    if len(cols) > limit:
        preview += ", ..."
    return preview


def normalize_finance(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    df = df.loc[:, ~df.columns.duplicated()].copy()

    required = {"Data", "Conta", "Categoria", "Receita", "Despesa", "Valor pago", "Natureza"}
    if not required.issubset(df.columns):
        missing = ", ".join(sorted(required - set(df.columns)))
        raise ValueError(f"Estrutura financeira incompleta. Faltam: {missing}")

    for col in ["Data", "Competência", "Vencimento", "Pagamento"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    valor_pago_raw = df["Valor pago"].astype(str).fillna("").str.strip()

    for col in ["Receita", "Despesa", "Desconto", "Multa", "Juros", "Valor pago"]:
        if col in df.columns:
            df[col] = df[col].map(parse_money)

    for col in ["Conta", "Categoria", "Descrição", "Fornecedor", "Parcela", "Forma pagamento", "Documento", "Natureza", "Observação"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    df["Categoria"] = df["Categoria"].replace("", "Transferência")
    df["É Transferência"] = df["Categoria"].str.contains("transfer", case=False, na=False)
    df["É Em Aberto"] = df["Pagamento"].isna() & ~df["É Transferência"]
    df["Tem Valor Pago"] = valor_pago_raw.ne("")
    df["Data de referência"] = df["Pagamento"].fillna(df["Data"])
    df["Competência de referência"] = df["Competência"].fillna(df["Data"])
    df["Valor Realizado"] = df["Receita"].fillna(0.0) + df["Despesa"].fillna(0.0)
    df["Valor Absoluto"] = df["Valor Realizado"].abs()
    return df


def normalize_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    df = df.loc[:, ~df.columns.duplicated()].copy()

    required = {"Data e hora", "Venda", "Status da venda", "Cliente", "Animal", "Espécie", "Raça", "Tipo do Item", "Grupo", "Produto/serviço", "Líquido"}
    if not required.issubset(df.columns):
        missing = ", ".join(sorted(required - set(df.columns)))
        raise ValueError(f"Estrutura comercial incompleta. Faltam: {missing}")

    for col in ["Data e hora", "Data baixa"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    text_cols = [
        "Status da venda",
        "Forma pagamento",
        "Funcionário",
        "Cliente",
        "Animal",
        "Espécie",
        "Raça",
        "Tipo do Item",
        "Grupo",
        "Produto/serviço",
        "Observações",
        "Sexo",
        "Sexo.1",
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()
        else:
            df[col] = ""

    for col in ["Venda", "Valor Unitário", "Bruto", "Desconto", "Líquido", "Código", "Quantidade"]:
        if col in df.columns:
            if col == "Venda":
                df[col] = df[col].astype(str).str.replace(".0", "", regex=False).str.strip()
            elif col == "Quantidade":
                df[col] = pd.to_numeric(df[col].map(parse_money), errors="coerce").fillna(0.0)
            else:
                df[col] = df[col].map(parse_money)

    df["Cliente Chave"] = df["Cliente"].astype(str).str.upper().str.strip()
    df["Cliente Exibicao"] = df["Cliente"].map(abbreviate_name)
    df["Funcionario Chave"] = df["Funcionário"].astype(str).str.upper().str.strip() if "Funcionário" in df.columns else ""
    df["Funcionario Exibicao"] = df["Funcionário"].map(abbreviate_name) if "Funcionário" in df.columns else ""

    if "Sexo.1" in df.columns:
        df = df.rename(columns={"Sexo.1": "Sexo do Animal"})
    elif "Sexo" in df.columns:
        df = df.rename(columns={"Sexo": "Sexo do Animal"})

    if "Sexo" in df.columns:
        df = df.drop(columns=["Sexo"])

    drop_cols = ["Código", "CPF", "CEP", "Endereço", "Número", "Bairro", "Email", "Celular", "Observações"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])
    df = df.loc[:, ~df.columns.duplicated()].copy()

    if "Sexo do Animal" not in df.columns:
        df["Sexo do Animal"] = ""

    df["Data de referência"] = df["Data e hora"]
    df["Status Normalizado"] = df["Status da venda"].astype(str).str.strip().str.lower()
    df["Realizada"] = df["Status Normalizado"].isin({"baixado", "baixa parcial"})
    return df


def resolve_period(start_ref: date, end_ref: date, choice: str, custom_start: date, custom_end: date) -> tuple[date, date]:
    if choice == "Personalizado":
        return custom_start, custom_end
    delta_days = PERIOD_PRESETS.get(choice, 29)
    end_date = end_ref
    start_date = end_date - timedelta(days=delta_days)
    return start_date, end_date


def filter_by_period(df: pd.DataFrame, date_col: str, start_date: date, end_date: date) -> pd.DataFrame:
    if df.empty or date_col not in df.columns:
        return df.iloc[0:0].copy()
    mask = df[date_col].dt.date.between(start_date, end_date)
    return df.loc[mask].copy()


def decendio_label(day_value: float | int | None) -> str:
    if pd.isna(day_value):
        return "N/A"
    day = int(day_value)
    if day <= 10:
        return "1º Decêndio"
    if day <= 20:
        return "2º Decêndio"
    return "3º Decêndio"


def share_of_total(value: float, total: float) -> float:
    return (value / total * 100) if total else 0.0


def escape_markdown_currency(text: str) -> str:
    return str(text).replace("$", "\\$")


def currency_text(value: float) -> str:
    return brl(value).replace("$", "&#36;")


def finance_scope(df: pd.DataFrame, start_date: date, end_date: date, mode: str) -> pd.DataFrame:
    date_col = "Data de referência" if mode == "Caixa realizado" else "Data"
    if date_col not in df.columns:
        return df.iloc[0:0].copy()
    scoped = df.loc[df[date_col].dt.date.between(start_date, end_date)].copy()
    scoped["Data filtro"] = scoped[date_col]
    return scoped


def finance_split_summary(df: pd.DataFrame) -> dict[str, float]:
    receitas = df.loc[df["Natureza"].str.lower() == "receita", "Valor Absoluto"]
    despesas = df.loc[df["Natureza"].str.lower() == "despesa", "Valor Absoluto"]
    return {
        "receitas_count": int((df["Natureza"].str.lower() == "receita").sum()),
        "receitas_value": float(receitas.sum()),
        "despesas_count": int((df["Natureza"].str.lower() == "despesa").sum()),
        "despesas_value": float(despesas.sum()),
    }


def render_alert_box(message: str) -> None:
    st.markdown(
        f"""
        <div style="background:#fff4f4;border:1px solid #f2c6c6;border-left:6px solid #d93025;border-radius:12px;padding:0.8rem 1rem;margin:0.35rem 0;color:#7a1f1f;">
          {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def finance_metrics(df: pd.DataFrame, mapping: dict[str, str], mode: str) -> dict:
    em_aberto = df.loc[df["É Em Aberto"]].copy()
    base_paid = df.loc[~df["É Transferência"] & ~df["É Em Aberto"] & df["Tem Valor Pago"]].copy()
    sem_valor_pago = df.loc[~df["Tem Valor Pago"] & ~df["É Transferência"] & ~df["É Em Aberto"]].copy()
    if mode == "Caixa realizado":
        analysis_base = base_paid.copy()
    else:
        analysis_base = df.loc[~df["É Transferência"]].copy()
    receitas = float(analysis_base.loc[analysis_base["Natureza"].str.lower() == "receita", "Valor Absoluto"].sum())
    despesas = float(analysis_base.loc[analysis_base["Natureza"].str.lower() == "despesa", "Valor Absoluto"].sum())
    resultado = receitas - despesas
    total_lancamentos = int(analysis_base.shape[0])
    transferencias = int(df["É Transferência"].sum())
    transferencias_entrada = float(df.loc[df["É Transferência"] & (df["Valor Realizado"] > 0), "Valor Absoluto"].sum())
    transferencias_saida = float(df.loc[df["É Transferência"] & (df["Valor Realizado"] < 0), "Valor Absoluto"].sum())
    aberto_count = int(em_aberto.shape[0])
    aberto_value = float(em_aberto["Valor Absoluto"].sum())
    excluido_base = analysis_base.loc[
        analysis_base.apply(lambda row: finance_bucket(row.get("Categoria", ""), row.get("Natureza", ""), mapping)[0] == "EXCLUIR", axis=1)
    ].copy()
    excluido_count = int(excluido_base.shape[0])
    excluido_value = float(excluido_base["Valor Absoluto"].sum())
    em_aberto_split = finance_split_summary(em_aberto)
    sem_valor_pago_split = finance_split_summary(sem_valor_pago)
    return {
        "realizado": analysis_base,
        "receitas": receitas,
        "despesas": despesas,
        "resultado": resultado,
        "total_lancamentos": total_lancamentos,
        "transferencias": transferencias,
        "transferencias_entrada": transferencias_entrada,
        "transferencias_saida": transferencias_saida,
        "aberto_count": aberto_count,
        "aberto_value": aberto_value,
        "em_aberto": em_aberto,
        "em_aberto_split": em_aberto_split,
        "sem_valor_pago_count": int(sem_valor_pago.shape[0]),
        "sem_valor_pago_value": float(sem_valor_pago["Valor Absoluto"].sum()),
        "sem_valor_pago": sem_valor_pago,
        "sem_valor_pago_split": sem_valor_pago_split,
        "excluido_count": excluido_count,
        "excluido_value": excluido_value,
        "excluido_base": excluido_base,
    }


def sales_metrics(df: pd.DataFrame) -> dict:
    realizados = df.loc[df["Realizada"]].copy()
    if realizados.empty:
        return {
            "realizados": realizados,
            "vendas": pd.DataFrame(),
            "total_faturamento": 0.0,
            "total_vendas": 0,
            "total_itens": 0.0,
            "pa": 0.0,
            "ticket_medio": 0.0,
            "clientes_pontuais": 0,
            "clientes_recorrentes": 0,
            "faturamento_recorrente": 0.0,
        }

    vendas = (
        realizados.groupby("Venda", as_index=False)
        .agg(
            **{
                "Data realizada": ("Data de referência", "first"),
                "Cliente Chave": ("Cliente Chave", "first"),
                "Cliente": ("Cliente Exibicao", "first"),
                "Funcionario Chave": ("Funcionario Chave", "first"),
                "Vendedora": ("Funcionario Exibicao", "first"),
                "Animal": ("Animal", first_non_empty),
                "Espécie": ("Espécie", first_non_empty),
                "Sexo do Animal": ("Sexo do Animal", first_non_empty),
                "Raça": ("Raça", first_non_empty),
                "Forma pagamento": ("Forma pagamento", join_unique),
                "Itens": ("Quantidade", "sum"),
                "Bruto": ("Bruto", "sum"),
                "Desconto": ("Desconto", "sum"),
                "Faturamento": ("Líquido", "sum"),
            }
        )
    )

    total_faturamento = float(vendas["Faturamento"].sum())
    total_vendas = int(vendas.shape[0])
    total_itens = int(realizados.shape[0])
    pa = total_itens / total_vendas if total_vendas else 0.0
    ticket_medio = total_faturamento / total_vendas if total_vendas else 0.0

    clientes = (
        vendas.groupby("Cliente Chave", as_index=False)
        .agg(Cliente=("Cliente", "first"), Vendas=("Venda", "count"), Faturamento=("Faturamento", "sum"))
        .sort_values(["Faturamento", "Vendas"], ascending=[False, False])
    )
    clientes["% Faturamento"] = (clientes["Faturamento"] / total_faturamento * 100) if total_faturamento else 0.0
    clientes["Recorrente"] = np.where(clientes["Vendas"] > 1, "Sim", "Não")

    clientes_pontuais = int((clientes["Vendas"] == 1).sum())
    clientes_recorrentes = int((clientes["Vendas"] > 1).sum())
    faturamento_recorrente = float(clientes.loc[clientes["Vendas"] > 1, "Faturamento"].sum())

    return {
        "realizados": realizados,
        "vendas": vendas,
        "clientes": clientes,
        "total_faturamento": total_faturamento,
        "total_vendas": total_vendas,
        "total_itens": total_itens,
        "pa": pa,
        "ticket_medio": ticket_medio,
        "clientes_pontuais": clientes_pontuais,
        "clientes_recorrentes": clientes_recorrentes,
        "faturamento_recorrente": faturamento_recorrente,
    }


FINANCE_REVENUE_SUBGROUPS = {
    "Receita de vendas": ["Vendas"],
    "Outras receitas": ["Adiantamento de clientes"],
}

FINANCE_EXPENSE_SUBGROUPS = {
    "Tributos": ["Simples nacional", "Taxas e contribuições"],
    "Custos": [
        "Veterinários terceirizados",
        "Fornecedores de produtos",
        "Exames de Ultrassom",
        "Exames cardiológicos - ECG/ECO",
        "Laboratório clínico",
        "LABORATÓRIOS",
        "RaioX",
    ],
    "Despesas administrativas": [
        "Aluguel",
        "Contabilidade",
        "Telefone e Internet",
        "Água",
        "Energia elétrica",
        "SEGUROS",
        "Sistema de Gestão SIMPLESVET",
        "Recolhimento resíduos",
        "Material de escritorio",
        "Material de limpeza",
    ],
    "Despesas operacionais": [
        "Publicidade",
        "Cursos e treinamentos",
        "Supermercado",
        "Manutenção e Reparos",
        "Uso e Consumo",
        "Estacionamento",
        "Despesas com transporte (Uber, Taxi, etc)",
        "Despesas C/ Correios",
    ],
    "Despesas trabalhistas": [
        "Salários",
        "Benefícios",
        "Adiantamento de salários",
        "Comissões",
        "FGTS",
        "IRRF",
    ],
    "Investimento em imobilizado": [],
}

FINANCE_SUBGROUP_OPTIONS = {
    "RECEITA": ["Receita de vendas", "Outras receitas", "Receitas não parametrizadas"],
    "DESPESA": [
        "Tributos",
        "Custos",
        "Despesas administrativas",
        "Despesas operacionais",
        "Despesas trabalhistas",
        "Investimento em imobilizado",
        "Despesas não parametrizadas",
    ],
}
FINANCE_EXCLUDED_SUBGROUP = "Societário / Investimentos"
FINANCE_SUBGROUP_PARENT = {
    subgroup: group
    for group, subgroup_list in FINANCE_SUBGROUP_OPTIONS.items()
    for subgroup in subgroup_list
}


def build_default_finance_mapping() -> dict[str, str]:
    mapping = {}
    for subgroup, categories in FINANCE_REVENUE_SUBGROUPS.items():
        for category in categories:
            mapping[str(category).strip()] = subgroup
    for subgroup, categories in FINANCE_EXPENSE_SUBGROUPS.items():
        for category in categories:
            mapping[str(category).strip()] = subgroup
    for category in ["Adiantamento a socio", "Adiantamento a sócio", "Distribuição de Lucros", "Distribuição de lucros"]:
        mapping[category] = FINANCE_EXCLUDED_SUBGROUP
    return mapping


DEFAULT_FINANCE_MAPPING = build_default_finance_mapping()


def save_finance_mapping(mapping: dict[str, str]) -> None:
    cleaned = {
        str(category).strip(): str(group).strip()
        for category, group in mapping.items()
        if str(category).strip() and str(group).strip()
    }
    FINANCE_MAP_FILE.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")


def load_finance_mapping() -> dict[str, str]:
    if not FINANCE_MAP_FILE.exists():
        save_finance_mapping(DEFAULT_FINANCE_MAPPING)
        return DEFAULT_FINANCE_MAPPING.copy()
    try:
        data = json.loads(FINANCE_MAP_FILE.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    merged = DEFAULT_FINANCE_MAPPING.copy()
    merged.update(
        {
            str(category).strip(): str(group).strip()
            for category, group in data.items()
            if str(category).strip() and str(group).strip()
        }
    )
    return merged


def default_finance_subgroup(nature: str) -> str:
    return "Receitas não parametrizadas" if str(nature or "").strip().lower() == "receita" else "Despesas não parametrizadas"


def finance_bucket(category: str, nature: str, mapping: dict[str, str] | None = None) -> tuple[str, str]:
    cat = re.sub(r"\s+", " ", str(category or "")).strip()
    nat = str(nature or "").strip().lower()

    if not cat or cat.lower() in {"nan", "none"}:
        return "DESPESA", "Despesas não parametrizadas"

    normalized = cat.lower()
    if any(
        token in normalized
        for token in ["lucro", "distribuição", "distribuicao", "socio", "sócio", "adiantamento a socio", "adiantamento a sócio"]
    ):
        return "EXCLUIR", FINANCE_EXCLUDED_SUBGROUP

    active_mapping = mapping or DEFAULT_FINANCE_MAPPING
    subgroup = active_mapping.get(cat, default_finance_subgroup(nature))

    if subgroup == FINANCE_EXCLUDED_SUBGROUP:
        return "EXCLUIR", subgroup
    if subgroup in FINANCE_SUBGROUP_PARENT:
        return FINANCE_SUBGROUP_PARENT[subgroup], subgroup
    return ("RECEITA", subgroup) if nat == "receita" else ("DESPESA", subgroup)


def build_finance_dre(realizado: pd.DataFrame, mapping: dict[str, str]) -> dict:
    if realizado.empty:
        return {
            "base": pd.DataFrame(),
            "faturamento_base": 0.0,
            "receita_total": 0.0,
            "despesa_total": 0.0,
            "resultado": 0.0,
            "groups": {},
        }

    base = realizado.copy()
    base[["Grupo DRE", "Subgrupo DRE"]] = base.apply(
        lambda row: pd.Series(finance_bucket(row.get("Categoria", ""), row.get("Natureza", ""), mapping)),
        axis=1,
    )
    base = base.loc[base["Grupo DRE"] != "EXCLUIR"].copy()
    if base.empty:
        return {
            "base": pd.DataFrame(),
            "faturamento_base": 0.0,
            "receita_total": 0.0,
            "despesa_total": 0.0,
            "resultado": 0.0,
            "groups": {},
        }

    faturamento_base = float(base.loc[base["Grupo DRE"] == "RECEITA", "Valor Absoluto"].sum())
    despesa_total = float(base.loc[base["Grupo DRE"] == "DESPESA", "Valor Absoluto"].sum())
    pivot = (
        base.groupby(["Grupo DRE", "Subgrupo DRE", "Categoria"], as_index=False)["Valor Absoluto"]
        .sum()
        .sort_values(["Grupo DRE", "Subgrupo DRE", "Valor Absoluto"], ascending=[True, True, False])
    )

    groups = {}
    for group, subgroup_order in FINANCE_SUBGROUP_OPTIONS.items():
        group_df = base.loc[base["Grupo DRE"] == group].copy()
        group_total = float(group_df["Valor Absoluto"].sum())
        subgroup_cards = []
        for subgroup in subgroup_order:
            subgroup_df = pivot.loc[(pivot["Grupo DRE"] == group) & (pivot["Subgrupo DRE"] == subgroup)].copy()
            subgroup_total = float(subgroup_df["Valor Absoluto"].sum())
            if subgroup_total <= 0:
                continue
            subgroup_df["% do grupo"] = subgroup_df["Valor Absoluto"].apply(lambda value: share_of_total(float(value), group_total))
            subgroup_df["% do faturamento"] = subgroup_df["Valor Absoluto"].apply(
                lambda value: share_of_total(float(value), faturamento_base)
            )
            subgroup_cards.append(
                {
                    "name": subgroup,
                    "total": subgroup_total,
                    "share_faturamento": share_of_total(subgroup_total, faturamento_base),
                    "share_group": share_of_total(subgroup_total, group_total),
                    "table": subgroup_df.rename(columns={"Valor Absoluto": "Valor"})[
                        ["Categoria", "Valor", "% do grupo", "% do faturamento"]
                    ],
                }
            )
        groups[group] = {
            "total": group_total,
            "share_faturamento": share_of_total(group_total, faturamento_base),
            "subgroups": subgroup_cards,
        }

    receita_total = float(base.loc[base["Grupo DRE"] == "RECEITA", "Valor Absoluto"].sum())
    return {
        "base": base,
        "faturamento_base": faturamento_base,
        "receita_total": receita_total,
        "despesa_total": despesa_total,
        "resultado": receita_total - despesa_total,
        "groups": groups,
    }


def finance_category_catalog(full_df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    if full_df.empty:
        return pd.DataFrame(columns=["Categoria", "Natureza", "Subgrupo Atual"])
    catalog = (
        full_df.loc[~full_df["É Transferência"] & ~full_df["É Em Aberto"], ["Categoria", "Natureza"]]
        .drop_duplicates()
        .copy()
    )
    catalog["Natureza"] = catalog["Natureza"].astype(str).str.strip().str.lower()
    catalog["Subgrupo Atual"] = catalog.apply(
        lambda row: finance_bucket(row["Categoria"], row["Natureza"], mapping)[1],
        axis=1,
    )
    catalog["Natureza"] = catalog["Natureza"].map({"receita": "Receita", "despesa": "Despesa"}).fillna("Despesa")
    return catalog.sort_values(["Natureza", "Categoria"]).reset_index(drop=True)


# =========================
# Renderização Financeira
# =========================

def render_finance_dre_panel(dre: dict) -> None:
    st.markdown("**DRE simplificada**")
    summary_df = pd.DataFrame(
        [
            {
                "Linha": "Receita",
                "Valor": dre["receita_total"],
                "% do faturamento": share_of_total(dre["receita_total"], dre["faturamento_base"]),
            },
            {
                "Linha": "Despesa",
                "Valor": dre["despesa_total"],
                "% do faturamento": share_of_total(dre["despesa_total"], dre["faturamento_base"]),
            },
            {
                "Linha": "Lucro do período",
                "Valor": dre["resultado"],
                "% do faturamento": share_of_total(dre["resultado"], dre["faturamento_base"]),
            },
        ]
    )
    st.dataframe(
        summary_df.style.format({"Valor": brl, "% do faturamento": "{:.2f}%"}),
        use_container_width=True,
        hide_index=True,
    )

    for group_name, title in [("RECEITA", "Receita"), ("DESPESA", "Despesa")]:
        st.markdown(f"**{title}**")
        group_data = dre["groups"].get(group_name, {})
        if not group_data or not group_data.get("subgroups"):
            st.info("Nenhum grupo encontrado para este recorte.")
            continue
        for subgroup in group_data["subgroups"]:
            with st.expander(
                f"{subgroup['name']} | {brl(subgroup['total'])} | {subgroup['share_faturamento']:.2f}% do faturamento",
                expanded=subgroup["share_faturamento"] >= 15,
            ):
                st.dataframe(
                    subgroup["table"].style.format(
                        {
                            "Valor": brl,
                            "% do grupo": "{:.2f}%",
                            "% do faturamento": "{:.2f}%",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )


def render_finance_mapping_tab(full_df: pd.DataFrame, mapping: dict[str, str]) -> None:
    st.markdown("**Parametrização financeira**")
    st.caption("Categorias novas ou antigas podem ser reclassificadas aqui. O mapeamento fica salvo no projeto.")

    catalog = finance_category_catalog(full_df, mapping)
    if catalog.empty:
        st.info("Não há categorias disponíveis para parametrização nesta base.")
        return

    unmapped_count = int(
        catalog["Subgrupo Atual"].isin({"Receitas não parametrizadas", "Despesas não parametrizadas"}).sum()
    )
    if unmapped_count > 0:
        st.warning(f"Existem {unmapped_count} categorias ainda não parametrizadas.")

    search = st.text_input("Buscar categoria", key="finance_mapping_search")
    nature_filter = st.radio(
        "Filtrar por natureza",
        ["Todas", "Receita", "Despesa"],
        horizontal=True,
        key="finance_mapping_nature",
    )

    visible = catalog.copy()
    if nature_filter != "Todas":
        visible = visible.loc[visible["Natureza"] == nature_filter].copy()
    if search:
        visible = visible.loc[visible["Categoria"].str.contains(search, case=False, na=False)].copy()

    if visible.empty:
        st.info("Nenhuma categoria encontrada com esse filtro.")
        return

    updated_mapping = mapping.copy()
    for _, row in visible.iterrows():
        group_key = "RECEITA" if row["Natureza"] == "Receita" else "DESPESA"
        options = FINANCE_SUBGROUP_OPTIONS[group_key] + [FINANCE_EXCLUDED_SUBGROUP]
        current_value = str(row["Subgrupo Atual"])
        safe_key = re.sub(r"[^a-zA-Z0-9_]+", "_", f"{row['Categoria']}_{row['Natureza']}".lower())
        c1, c2 = st.columns([1.8, 1.2])
        c1.markdown(f"**{row['Categoria']}**  \nNatureza: {row['Natureza']}")
        selected = c2.selectbox(
            "Grupo gerencial",
            options,
            index=options.index(current_value) if current_value in options else options.index(default_finance_subgroup(row["Natureza"])),
            key=f"finance_map_{safe_key}",
            label_visibility="collapsed",
        )
        updated_mapping[str(row["Categoria"])] = selected

    b1, b2 = st.columns(2)
    if b1.button("Salvar parametrização", use_container_width=True):
        save_finance_mapping(updated_mapping)
        st.success("Parametrização financeira salva.")
        st.rerun()

    if b2.button("Limpar mapeamentos sem uso nesta base", use_container_width=True):
        in_use = set(catalog["Categoria"])
        pruned = {category: group for category, group in updated_mapping.items() if category in in_use}
        save_finance_mapping(pruned)
        st.success("Mapeamentos fora da base atual foram removidos.")
        st.rerun()


def finance_reflections_markdown(dre: dict, expense_rank: pd.DataFrame, metrics: dict) -> str:
    reflections = []
    expense_groups = dre["groups"].get("DESPESA", {}).get("subgroups", [])
    if expense_groups:
        main_group = max(expense_groups, key=lambda item: item["total"])
        reflections.append(
            f"- **Alto valor em {main_group['name']}:** essa faixa consumiu **{main_group['share_faturamento']:.2f}% do faturamento**. "
            f"O que puxou esse bloco neste período e quanto disso deve se repetir no próximo mês?"
        )
    if not expense_rank.empty and dre["faturamento_base"] > 0:
        top_expense = expense_rank.iloc[0]
        reflections.append(
            f"- **{top_expense['Categoria']} em foco:** sozinha representou **{share_of_total(float(top_expense['Valor Absoluto']), dre['faturamento_base']):.2f}% do faturamento**. "
            "Foi um evento pontual ou essa categoria virou um novo patamar de gasto?"
        )
    margin = share_of_total(dre["resultado"], dre["faturamento_base"])
    if margin < 15:
        reflections.append(
            f"- **Margem apertada:** o período fechou com **{margin:.2f}%** de resultado sobre o faturamento. "
            "Onde existe espaço real para renegociar custo sem comprometer a operação clínica?"
        )
    else:
        reflections.append(
            f"- **Resultado saudável:** a operação reteve **{margin:.2f}%** do faturamento como resultado. "
            "Quais despesas precisam continuar sob disciplina para preservar essa margem nos próximos ciclos?"
        )
    if metrics["transferencias"] > 0:
        reflections.append(
            f"- **Fluxo entre contas:** houve **{metrics['transferencias']} transferências** no período. "
            "Esse giro entre bancos está apoiando a operação ou sinalizando necessidade recorrente de ajuste de caixa?"
        )
    return "\n".join(reflections)


def render_finance_open_table(df: pd.DataFrame, title: str) -> None:
    if df.empty:
        return
    st.markdown(f"**{title}**")
    for nature, label in [("receita", "Receitas em aberto"), ("despesa", "Despesas em aberto")]:
        table = df.loc[df["Natureza"].str.lower() == nature].copy()
        with st.expander(label):
            if table.empty:
                st.info(f"Nenhum lançamento de {label.lower()} neste período.")
                continue
            table["Data exibição"] = table["Data filtro"].dt.strftime("%d/%m/%Y").fillna("")
            st.dataframe(
                table[["Data exibição", "Categoria", "Descrição", "Receita", "Despesa"]]
                .rename(columns={"Data exibição": "Data"})
                .style.format({"Receita": brl, "Despesa": brl}),
                use_container_width=True,
                hide_index=True,
            )


def render_finance_top_expense_categories(base: pd.DataFrame) -> None:
    expense_rows = base.loc[base["Natureza"].str.lower() == "despesa"].copy()
    if expense_rows.empty:
        return
    top_categories = (
        expense_rows.groupby("Categoria", as_index=False)["Valor Absoluto"]
        .sum()
        .sort_values("Valor Absoluto", ascending=False)
        .head(5)
    )
    st.markdown("**Top 5 categorias de despesas**")
    for _, row in top_categories.iterrows():
        detail = expense_rows.loc[expense_rows["Categoria"] == row["Categoria"]].copy()
        detail["Data exibição"] = detail["Data filtro"].dt.strftime("%d/%m/%Y").fillna("")
        with st.expander(f"{row['Categoria']} | {brl(float(row['Valor Absoluto']))}"):
            st.dataframe(
                detail[["Data exibição", "Descrição", "Valor Absoluto"]].rename(
                    columns={"Data exibição": "Data", "Valor Absoluto": "Valor"}
                ).style.format({"Valor": brl}),
                use_container_width=True,
                hide_index=True,
            )


def render_finance_section(full_df: pd.DataFrame, start_date: date, end_date: date) -> None:
    st.markdown('<div class="section-title">🐾 Financeiro realizado</div>', unsafe_allow_html=True)
    finance_mode = st.radio(
        "Leitura financeira",
        ["Caixa realizado", "Competência do período"],
        horizontal=True,
        key="finance_mode",
    )
    note = (
        "Transferências separadas. Esta visão mostra apenas o que já foi pago/recebido."
        if finance_mode == "Caixa realizado"
        else "Transferências separadas. Esta visão considera a competência do período, incluindo valores em aberto."
    )
    st.markdown(f'<div class="section-note">{note}</div>', unsafe_allow_html=True)

    mapping = load_finance_mapping()
    df = finance_scope(full_df, start_date, end_date, finance_mode)
    metrics = finance_metrics(df, mapping, finance_mode)
    realizado = metrics["realizado"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receitas", brl(metrics["receitas"]))
    c2.metric("Despesas", brl(metrics["despesas"]))
    c3.metric("Resultado", brl(metrics["resultado"]))
    c4.metric("Lançamentos no período", f"{metrics['total_lancamentos']}")

    t1, t2, t3 = st.columns(3)
    t1.metric("Transferências", f"{metrics['transferencias']}")
    t2.metric("Entradas de transferência", brl(metrics["transferencias_entrada"]))
    t3.metric("Saídas de transferência", brl(metrics["transferencias_saida"]))

    if metrics["aberto_count"] > 0:
        split = metrics["em_aberto_split"]
        render_alert_box(
            f"🚨 Em aberto no período: {metrics['aberto_count']} lançamentos, somando {currency_text(metrics['aberto_value'])}. "
            f"Receitas: {split['receitas_count']} ({currency_text(split['receitas_value'])}). "
            f"Despesas: {split['despesas_count']} ({currency_text(split['despesas_value'])})."
        )
    if metrics["sem_valor_pago_count"] > 0:
        split = metrics["sem_valor_pago_split"]
        render_alert_box(
            f"🚨 Sem valor pago preenchido: {metrics['sem_valor_pago_count']} lançamentos, somando {currency_text(metrics['sem_valor_pago_value'])}. "
            f"Receitas: {split['receitas_count']} ({currency_text(split['receitas_value'])}). "
            f"Despesas: {split['despesas_count']} ({currency_text(split['despesas_value'])})."
        )
    if metrics["excluido_count"] > 0:
        render_alert_box(
            f"🚨 Foram encontrados {metrics['excluido_count']} movimentos não operacionais/societários, somando {currency_text(metrics['excluido_value'])}. "
            + (
                "Na competência eles aparecem para completar o período."
                if finance_mode == "Competência do período"
                else "Eles entram no pago do período, mas ficam fora da DRE operacional."
            )
        )

    if finance_mode == "Caixa realizado":
        render_finance_open_table(metrics["em_aberto"], "Quadro simplificado de receitas e despesas em aberto")

    view_tab, config_tab = st.tabs(["Análise DRE", "Parametrização"])

    with config_tab:
        render_finance_mapping_tab(full_df, mapping)

    with view_tab:
        if realizado.empty:
            st.info("Não encontrei lançamentos financeiros realizados no período selecionado.")
            return

        dre = build_finance_dre(realizado, mapping)
        render_finance_dre_panel(dre)

        expense_rank = (
            dre["base"]
            .loc[dre["base"]["Natureza"].str.lower() == "despesa"]
            .groupby("Categoria", as_index=False)["Valor Absoluto"]
            .sum()
            .sort_values("Valor Absoluto", ascending=False)
            .reset_index(drop=True)
        )

        st.markdown("**Ranking de despesas**")
        if expense_rank.empty:
            st.info("Nenhuma despesa encontrada no período.")
        else:
            top_expense_chart = expense_rank.head(10).copy()
            fig = px.bar(
                top_expense_chart.sort_values("Valor Absoluto"),
                x="Valor Absoluto",
                y="Categoria",
                orientation="h",
                text="Valor Absoluto",
                color="Valor Absoluto",
                color_continuous_scale=["#eef4ff", "#89a7e0", "#2f4f8f"],
            )
            fig.update_traces(texttemplate="%{text:$,.2f}", textposition="outside")
            fig.update_layout(
                height=390,
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Valor",
                yaxis_title="",
            )
            st.plotly_chart(fig, use_container_width=True)
        render_finance_top_expense_categories(dre["base"])

        top_expense_cat = "sem categoria"
        top_expense_value = 0.0
        if not expense_rank.empty:
            top_expense_cat = str(expense_rank.iloc[0]["Categoria"])
            top_expense_value = float(expense_rank.iloc[0]["Valor Absoluto"])

        st.markdown("**Resumo executivo financeiro**")
        st.markdown(
            "\n".join(
                [
                    f"- **Receita realizada:** {brl(dre['receita_total'])}",
                    f"- **Despesa realizada:** {brl(dre['despesa_total'])}",
                    f"- **Resultado do período:** {brl(dre['resultado'])} ({share_of_total(dre['resultado'], dre['faturamento_base']):.2f}% do faturamento)",
                    f"- **Maior pressão de custo:** {top_expense_cat} ({brl(top_expense_value)})",
                ]
            )
        )

        st.markdown("**Reflexões para melhoria**")
        st.markdown(finance_reflections_markdown(dre, expense_rank, metrics))


def sales_reflections_markdown(
    weekday_table: pd.DataFrame,
    metrics: dict,
    group_totals: pd.DataFrame,
    clientes_top5: pd.DataFrame,
) -> str:
    reflections = []
    active_days = weekday_table.loc[weekday_table["Qtd atendimentos"] > 0].copy()
    if not active_days.empty:
        best_tkm = active_days.loc[active_days["TKM"].idxmax()]
        best_pa = active_days.loc[active_days["P.A."].idxmax()]
        lowest_pa = active_days.loc[active_days["P.A."].idxmin()]
        reflections.append(
            f"- **Super {str(best_tkm['Dia da semana']).lower()}:** esse foi o dia com maior ticket médio "
            f"(**{brl(float(best_tkm['TKM']))}**). O que aconteceu de diferente nesse dia para sustentar esse valor?"
        )
        reflections.append(
            f"- **Produtividade em {str(best_pa['Dia da semana']).lower()}:** o P.A. chegou a **{float(best_pa['P.A.']):.2f}**. "
            "Qual combinação de atendimento, mix e abordagem fez esse resultado aparecer?"
        )
        reflections.append(
            f"- **Oportunidade em {str(lowest_pa['Dia da semana']).lower()}:** com P.A. de **{float(lowest_pa['P.A.']):.2f}**, "
            "a equipe está focando só em fechar o pedido principal ou existe espaço para ampliar o mix com a clínica cheia?"
        )
    if not group_totals.empty:
        top_group = group_totals.iloc[0]
        reflections.append(
            f"- **Grupo líder {top_group['Grupo']}:** concentrou **{share_of_total(float(top_group['Faturamento']), metrics['total_faturamento']):.2f}% do faturamento**. "
            "Como manter essa força sem depender demais de uma única frente de receita?"
        )
    if not clientes_top5.empty:
        top_client = clientes_top5.iloc[0]
        reflections.append(
            f"- **Cliente mais relevante:** {top_client['Cliente']} respondeu por **{top_client['% Faturamento']:.2f}% do faturamento**. "
            "A clínica está fidelizando bem a base ou concentrando receita em poucos nomes?"
        )
    return "\n".join(reflections[:4])


# =========================
# Renderização Comercial
# =========================

def render_sales_section(df: pd.DataFrame, full_df: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">🐶 Comercial realizado</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Somente vendas baixadas e baixadas parciais entram na leitura principal. Dados sensíveis foram removidos da exibição.</div>',
        unsafe_allow_html=True,
    )

    open_sales = (
        df.loc[df["Status da venda"].eq("Aberto")]
        .groupby("Venda", as_index=False)
        .agg(Faturamento=("Líquido", "sum"))
    )

    metrics = sales_metrics(df)
    vendas = metrics["vendas"]
    realizados = metrics["realizados"]

    if not open_sales.empty:
        st.info(
            f"Foram encontradas {open_sales.shape[0]} vendas em aberto no período, somando {brl(open_sales['Faturamento'].sum())}. "
            "Essas vendas ficam fora das análises principais."
        )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faturamento", brl(metrics["total_faturamento"]))
    c2.metric("Atendimentos", f"{metrics['total_vendas']}")
    c3.metric("P.A.", f"{metrics['pa']:.2f}")
    c4.metric("Ticket médio", brl(metrics["ticket_medio"]))

    c5, c6 = st.columns(2)
    c5.metric("Clientes pontuais", f"{metrics['clientes_pontuais']}")
    c6.metric("Clientes recorrentes", f"{metrics['clientes_recorrentes']}")

    if vendas.empty:
        st.info("Não encontrei vendas realizadas no período selecionado.")
        return

    compare_start = (pd.Timestamp(df["Data de referência"].min()) - pd.DateOffset(years=1)).date() if not full_df.empty and full_df["Data de referência"].notna().any() else None
    compare_end = (pd.Timestamp(df["Data de referência"].max()) - pd.DateOffset(years=1)).date() if not full_df.empty and full_df["Data de referência"].notna().any() else None
    if compare_start and compare_end:
        compare_df = full_df.loc[full_df["Data de referência"].dt.date.between(compare_start, compare_end)].copy()
    else:
        compare_df = pd.DataFrame()

    st.markdown("**Comparativo anual**")
    if compare_df.empty:
        st.info("Não encontrei uma base comparável de um ano anterior neste arquivo. O relatório segue sem sujar essa seção.")
    else:
        current_metrics = metrics
        previous_metrics = sales_metrics(compare_df)
        comp = pd.DataFrame(
            [
                ["Atendimentos", current_metrics["total_vendas"], previous_metrics["total_vendas"]],
                ["P.A.", current_metrics["pa"], previous_metrics["pa"]],
                ["Ticket médio", current_metrics["ticket_medio"], previous_metrics["ticket_medio"]],
                ["Faturamento", current_metrics["total_faturamento"], previous_metrics["total_faturamento"]],
            ],
            columns=["Indicador", "Atual_num", "Ano_anterior_num"],
        )
        comp["Variação"] = np.where(
            comp["Ano_anterior_num"] > 0,
            (comp["Atual_num"] - comp["Ano_anterior_num"]) / comp["Ano_anterior_num"] * 100,
            np.nan,
        )
        comp["Atual"] = comp.apply(lambda row: brl(row["Atual_num"]) if row["Indicador"] in {"Ticket médio", "Faturamento"} else f"{int(row['Atual_num'])}" if row["Indicador"] == "Atendimentos" else f"{row['Atual_num']:.2f}", axis=1)
        comp["Ano anterior"] = comp.apply(lambda row: brl(row["Ano_anterior_num"]) if row["Indicador"] in {"Ticket médio", "Faturamento"} else f"{int(row['Ano_anterior_num'])}" if row["Indicador"] == "Atendimentos" else f"{row['Ano_anterior_num']:.2f}", axis=1)
        st.dataframe(
            comp[["Indicador", "Atual", "Ano anterior", "Variação"]].style.format({"Variação": "{:.2f}%"}),
            use_container_width=True,
            hide_index=True,
        )

    sales_by_weekday = (
        realizados.assign(DiaSemana=realizados["Data de referência"].dt.day_name())
        .assign(DiaSemana=lambda d: d["DiaSemana"].map(DAY_NAME_PT))
        .groupby("DiaSemana", as_index=False)
        .agg(
            **{
                "Qtd atendimentos": ("Venda", "nunique"),
                "Valor líquido": ("Líquido", "sum"),
                "Itens": ("Venda", "size"),
            }
        )
    )
    sales_by_weekday["P.A."] = np.where(
        sales_by_weekday["Qtd atendimentos"] > 0,
        sales_by_weekday["Itens"] / sales_by_weekday["Qtd atendimentos"],
        0.0,
    )
    sales_by_weekday["TKM"] = np.where(
        sales_by_weekday["Qtd atendimentos"] > 0,
        sales_by_weekday["Valor líquido"] / sales_by_weekday["Qtd atendimentos"],
        0.0,
    )
    sales_by_weekday["DiaSemana"] = pd.Categorical(sales_by_weekday["DiaSemana"], categories=DAY_ORDER, ordered=True)
    sales_by_weekday = sales_by_weekday.sort_values("DiaSemana")

    st.markdown("**Mapa de calor por dia da semana**")
    weekday_table = (
        sales_by_weekday.rename(columns={"DiaSemana": "Dia da semana"})
        .set_index("Dia da semana")
        .reindex(DAY_ORDER)
        .fillna(0.0)
        .reset_index()
    )
    weekday_table = weekday_table[["Dia da semana", "Qtd atendimentos", "Valor líquido", "P.A.", "TKM"]]
    metric_cols = ["Qtd atendimentos", "Valor líquido", "P.A.", "TKM"]
    st.dataframe(
        weekday_table.style.format(
            {
                "Qtd atendimentos": "{:.0f}",
                "Valor líquido": brl,
                "P.A.": "{:.2f}",
                "TKM": brl,
            }
        ).background_gradient(cmap="Blues", subset=metric_cols),
        use_container_width=True,
        hide_index=True,
    )

    if not weekday_table.empty:
        active_days = weekday_table.loc[weekday_table["Qtd atendimentos"] > 0].copy()
        best_fat = active_days.loc[active_days["Valor líquido"].idxmax()] if not active_days.empty else weekday_table.iloc[0]
        best_tkm = active_days.loc[active_days["TKM"].idxmax()] if not active_days.empty else weekday_table.iloc[0]
        best_pa = active_days.loc[active_days["P.A."].idxmax()] if not active_days.empty else weekday_table.iloc[0]
        st.markdown("**Leitura rápida do calendário comercial**")
        st.markdown(
            "\n".join(
                [
                    f"- **Melhor dia de faturamento:** {best_fat['Dia da semana']} com **{brl(float(best_fat['Valor líquido']))}**.",
                    f"- **Melhor dia de P.A.:** {best_pa['Dia da semana']} com **{float(best_pa['P.A.']):.2f}**.",
                    f"- **Melhor dia de TKM:** {best_tkm['Dia da semana']} com **{brl(float(best_tkm['TKM']))}**.",
                    "- **Pergunta-chave:** o que pode ser replicado nesses dias fortes para manter essa performance ao longo da semana?",
                ]
            )
        )

    st.markdown("**Total por grupo**")
    group_totals = (
        realizados.groupby("Grupo", as_index=False)
        .agg(Faturamento=("Líquido", "sum"))
        .sort_values("Faturamento", ascending=False)
    )
    if not group_totals.empty:
        fig_groups = go.Figure(
            data=[go.Pie(labels=group_totals["Grupo"], values=group_totals["Faturamento"], hole=0.55, textinfo="label+percent")]
        )
        fig_groups.update_traces(marker=dict(colors=["#1f3a6d", "#5e7fc1", "#89a7e0", "#dbe6ff"]))
        fig_groups.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=10, b=30),
            legend=dict(orientation="h", y=-0.18, x=0),
            showlegend=True,
        )
        st.plotly_chart(fig_groups, use_container_width=True)

    st.markdown("**Ranking de produtos e serviços**")
    top_products = (
        realizados.groupby(["Produto/serviço", "Grupo"], as_index=False)
        .agg(Quantidade=("Quantidade", "sum"), Faturamento=("Líquido", "sum"))
        .sort_values("Faturamento", ascending=False)
    )
    if not top_products.empty:
        fig_products = px.bar(
            top_products.head(10).sort_values("Faturamento"),
            x="Faturamento",
            y="Produto/serviço",
            orientation="h",
            text="Faturamento",
            color="Faturamento",
            color_continuous_scale=["#eef4ff", "#89a7e0", "#2f4f8f"],
        )
        fig_products.update_traces(texttemplate="%{text:$,.2f}", textposition="outside")
        fig_products.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig_products, use_container_width=True)

    if not top_products.empty:
        st.markdown("**Tabela dos 10 maiores produtos e serviços**")
        st.dataframe(
            top_products.head(10)[["Produto/serviço", "Grupo", "Quantidade", "Faturamento"]].style.format(
                {"Quantidade": "{:.0f}", "Faturamento": brl}
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("**Performance por vendedora / atendente**")
    sellers = (
        realizados.loc[realizados["Funcionario Exibicao"].astype(str).str.strip() != ""]
        .groupby("Funcionario Exibicao", as_index=False)
        .agg(
            Vendedora=("Funcionario Exibicao", "first"),
            Atendimentos=("Venda", "nunique"),
            Faturamento=("Líquido", "sum"),
            Itens=("Venda", "size"),
        )
        .sort_values("Faturamento", ascending=False)
    )
    sellers["P.A."] = np.where(sellers["Atendimentos"] > 0, sellers["Itens"] / sellers["Atendimentos"], 0.0)
    sellers["Ticket Médio"] = np.where(sellers["Atendimentos"] > 0, sellers["Faturamento"] / sellers["Atendimentos"], 0.0)
    st.dataframe(
        sellers[["Vendedora", "Atendimentos", "Faturamento", "P.A.", "Ticket Médio"]].style.format(
            {
                "Faturamento": brl,
                "P.A.": "{:.2f}",
                "Ticket Médio": brl,
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("**Clientes mais recorrentes e peso no faturamento**")
    clientes = metrics["clientes"].copy()
    clientes_top5 = clientes.head(5).copy()
    st.dataframe(
        clientes_top5[["Cliente", "Vendas", "Faturamento", "% Faturamento", "Recorrente"]].style.format(
            {"Faturamento": brl, "% Faturamento": "{:.2f}%"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("**🐱 Perfil clínico da base**")
    raca_summary = (
        realizados.loc[realizados["Raça"].astype(str).str.strip() != ""]
        .groupby("Raça", as_index=False)
        .agg(Faturamento=("Líquido", "sum"))
        .sort_values("Faturamento", ascending=False)
    )
    especie_summary = (
        realizados.loc[realizados["Espécie"].astype(str).str.strip() != ""]
        .groupby("Espécie", as_index=False)
        .agg(Faturamento=("Líquido", "sum"))
        .sort_values("Faturamento", ascending=False)
    )
    sexo_summary = (
        realizados.loc[realizados["Sexo do Animal"].astype(str).str.strip() != ""]
        .groupby("Sexo do Animal", as_index=False)
        .agg(Faturamento=("Líquido", "sum"))
        .sort_values("Faturamento", ascending=False)
    )

    p1, p2, p3 = st.columns(3)
    for col, title, label_col, summary in [
        (p1, "Raça", "Raça", raca_summary),
        (p2, "Espécie", "Espécie", especie_summary),
        (p3, "Sexo do animal", "Sexo do Animal", sexo_summary),
    ]:
        with col:
            if summary.empty:
                st.info(f"Sem dados de {title.lower()} neste período.")
                continue
            fig_profile = go.Figure(
                data=[go.Pie(labels=summary.head(8)[label_col], values=summary.head(8)["Faturamento"], hole=0.5, textinfo="percent")]
            )
            fig_profile.update_traces(
                marker=dict(colors=["#1f3a6d", "#2f4f8f", "#5e7fc1", "#89a7e0", "#a9bef0", "#c9d7fb", "#dbe6ff", "#eef4ff"])
            )
            fig_profile.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=10), showlegend=True)
            st.markdown(f"**{title}**")
            st.plotly_chart(fig_profile, use_container_width=True)
            st.dataframe(summary.style.format({"Faturamento": brl}), use_container_width=True, hide_index=True)

    decendio = vendas.copy()
    decendio["Decêndio"] = decendio["Data realizada"].dt.day.apply(decendio_label)
    dec_summary = (
        decendio.groupby("Decêndio", as_index=False)
        .agg(Vendas=("Venda", "nunique"), Faturamento=("Faturamento", "sum"))
        .set_index("Decêndio")
        .reindex(["1º Decêndio", "2º Decêndio", "3º Decêndio"])
        .fillna(0.0)
        .reset_index()
    )
    dec_summary["% do faturamento"] = np.where(metrics["total_faturamento"] > 0, dec_summary["Faturamento"] / metrics["total_faturamento"] * 100, 0.0)
    dec_summary = dec_summary.sort_values("Faturamento", ascending=False).reset_index(drop=True)
    dec_summary["Ranking"] = np.arange(1, len(dec_summary) + 1)
    dec_summary["Destaque"] = np.select(
        [dec_summary["Ranking"] == 1, dec_summary["Ranking"] == len(dec_summary)],
        ["Melhor período", "Ponto baixo"],
        default="Faixa intermediária",
    )
    st.markdown("**Quadro por decêndio**")
    st.dataframe(
        dec_summary[["Ranking", "Decêndio", "Faturamento", "% do faturamento", "Destaque"]].style.format({"Faturamento": brl, "% do faturamento": "{:.2f}%"}),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("**Resumo executivo comercial**")
    top_client = ""
    if not clientes_top5.empty:
        top_client = str(clientes_top5.iloc[0]["Cliente"])
    top_products_labels = []
    if not top_products.empty:
        medal_map = {0: "🥇", 1: "🥈", 2: "🥉"}
        top_products_labels = [
            f"{medal_map.get(idx, f'{idx + 1}.')} {row['Produto/serviço']} ({brl(float(row['Faturamento']))})"
            for idx, (_, row) in enumerate(top_products.head(3).iterrows())
        ]
    faturamento_total = metrics["total_faturamento"] + float(open_sales["Faturamento"].sum()) if not open_sales.empty else metrics["total_faturamento"]
    atendimentos_total = metrics["total_vendas"] + int(open_sales.shape[0])
    summary_lines = [
        f"- **Faturamento realizado/total:** {brl(metrics['total_faturamento'])} / {brl(faturamento_total)}",
        f"- **Atendimentos realizados/total:** {metrics['total_vendas']} / {atendimentos_total}",
        f"- **Cliente mais relevante no recorte:** {top_client or 'sem cliente'}",
        f"- **P.A. / TKM:** {metrics['pa']:.2f} | {brl(metrics['ticket_medio'])}",
        f"- **Top produtos/serviços por faturamento:** {' | '.join(top_products_labels) if top_products_labels else 'sem item'}",
    ]
    st.markdown(escape_markdown_currency("\n".join(summary_lines)))

    st.markdown("**Reflexões para melhoria**")
    st.markdown(sales_reflections_markdown(weekday_table, metrics, group_totals, clientes_top5))


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="footer-box">
          <div class="footer-grid">
            <div class="footer-logo">{partner_logo_html()}</div>
            <div>
              <div class="footer-title">{PARTNER_NAME}</div>
              <div>Fechamento contábil e financeiro preparado para apresentação gerencial mensal.</div>
              <div class="footer-contact">
                <strong>WhatsApp:</strong> {PARTNER_WHATSAPP}<br>
                <strong>Email:</strong> {PARTNER_EMAIL}<br>
                <strong>CNPJ:</strong> {PARTNER_CNPJ}
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# App Principal
# =========================

st.set_page_config(page_title="CliVet | Relatório Gerencial", layout="wide")
inject_styles()
render_hero()

st.sidebar.header("Importação")
finance_upload = st.sidebar.file_uploader(
    "Financeiro",
    type=UPLOAD_TYPES,
    key="finance_upload",
    help="Estrutura-base esperada: Data, Conta, Categoria, Receita, Despesa, Valor pago e Natureza.",
)
sales_upload = st.sidebar.file_uploader(
    "Comercial",
    type=UPLOAD_TYPES,
    key="sales_upload",
    help="Estrutura-base esperada: Data e hora, Venda, Status da venda, Cliente, Grupo, Produto/serviço e Líquido.",
)

st.sidebar.header("Período")
period_choice = st.sidebar.selectbox("Filtro", list(PERIOD_PRESETS.keys()) + ["Personalizado"], index=1)
custom_start = st.sidebar.date_input("Início", value=date.today() - timedelta(days=29))
custom_end = st.sidebar.date_input("Fim", value=date.today())

st.sidebar.markdown("---")
st.sidebar.caption("Bases tratadas por estrutura, não por nome do arquivo. Comercial e financeiro permanecem independentes.")
st.sidebar.caption("Dados sensíveis do comercial são descartados antes da análise.")

finance_df = None
sales_df = None
finance_error = None
sales_error = None

if finance_upload is not None:
    try:
        raw_finance = read_uploaded_table(finance_upload)
        if detect_dataset_kind(raw_finance) == "financeiro":
            finance_df = normalize_finance(raw_finance)
        else:
            finance_error = (
                "O arquivo enviado no campo Financeiro não parece ter estrutura financeira. "
                f"Colunas encontradas: {columns_preview(raw_finance)}."
            )
    except Exception as exc:
        finance_error = str(exc)

if sales_upload is not None:
    try:
        raw_sales = read_uploaded_table(sales_upload)
        if detect_dataset_kind(raw_sales) == "comercial":
            sales_df = normalize_sales(raw_sales)
        else:
            sales_error = (
                "O arquivo enviado no campo Comercial não parece ter estrutura comercial. "
                f"Colunas encontradas: {columns_preview(raw_sales)}."
            )
    except Exception as exc:
        sales_error = str(exc)

if finance_error:
    st.sidebar.error(finance_error)
if sales_error:
    st.sidebar.error(sales_error)

if finance_df is None and sales_df is None:
    st.info("Suba a base financeira e/ou comercial para começar a leitura.")
    render_footer()
    st.stop()

available_end_dates = []
if finance_df is not None and finance_df["Data de referência"].notna().any():
    available_end_dates.append(finance_df["Data de referência"].max().date())
if sales_df is not None and sales_df["Data de referência"].notna().any():
    available_end_dates.append(sales_df["Data de referência"].max().date())
end_reference = max(available_end_dates) if available_end_dates else date.today()

start_date, end_date = resolve_period(end_reference, end_reference, period_choice, custom_start, custom_end)

st.markdown(
    f"""
    <div class="soft-card">
      <strong>Período analisado:</strong> {start_date.strftime("%d/%m/%Y")} até {end_date.strftime("%d/%m/%Y")}<br>
      <span style="color:#6b7a90;">Financeiro = realizado sem transferências | Comercial = vendas baixadas e baixas parciais</span>
    </div>
    """,
    unsafe_allow_html=True,
)

print_c1, print_c2 = st.columns([1, 4])
with print_c1:
    components.html(
        """
        <div style="display:flex;align-items:center;justify-content:flex-start;padding-top:2px;">
          <button
            onclick="window.parent.print()"
            style="
              background:#2f4f8f;color:white;border:none;border-radius:10px;
              padding:8px 12px;font-size:13px;font-weight:700;cursor:pointer;
            "
          >
            Exportar PDF
          </button>
        </div>
        """,
        height=42,
    )
with print_c2:
    st.markdown('<div class="export-note">A exportação abre a impressão nativa do navegador já com a página preparada para PDF em paisagem.</div>', unsafe_allow_html=True)

tab_financeiro, tab_comercial = st.tabs(["Financeiro", "Comercial"])

with tab_financeiro:
    if finance_df is not None:
        render_finance_section(finance_df, start_date, end_date)
    else:
        st.info("Nenhuma base financeira foi enviada.")

with tab_comercial:
    if sales_df is not None:
        sales_period = filter_by_period(sales_df, "Data de referência", start_date, end_date)
        render_sales_section(sales_period, sales_df)
    else:
        st.info("Nenhuma base comercial foi enviada.")

render_footer()
