import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict

# Define constants for the categories
MAIN_CATEGORIES = [
    "エネルギー関連", "クリーニング工場", "レンタル機として保有", "運送業", "下水関連",
    "化学製品工場", "化学薬品工場", "機械製造業", "工業", "産業廃棄物", "商業施設",
    "食品製造", "生コン", "製紙", "繊維製品", "畜産", "発電所"
]

SUB_CATEGORIES = [
    "ガラス", "ごみ処理施設", "ゴム製品", "シャーペンの芯製造工場", "ショッピングモール",
    "し尿処理場", "その他", "バイオガス", "バイオマス", "ビル", "ホテル",
    "メタン発酵残渣", "レジャー施設", "レンダリング", "移動脱水車", "飲料",
    "下水処理場", "化粧品", "外食", "学校", "給食センター", "漁業集落排水",
    "金属", "健康食品", "自動車・二輪", "樹脂", "浄化槽", "食肉加工",
    "食品加工", "食料品", "飲料", "水産加工", "精米", "製パン", "製菓",
    "製麵", "製薬", "洗剤", "染料", "繊維・衣料", "繊維製品", "調味料",
    "漬物", "電気・電子部品", "電力", "塗装", "塗装系排水処理", "塗料",
    "肉牛", "乳飲料", "乳牛（酪農）", "乳製品", "農業集落排水", "農業⇒公共下水",
    "廃プラ", "プラ再生工場", "発電所", "病院", "薬品", "油田", "溶剤",
    "養鶏", "養豚", "冷凍・チルド・中食"
]

def load_and_process_data(uploaded_file) -> pd.DataFrame:
    """Load and process the uploaded Excel file."""
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return None

def create_order_status_chart(df: pd.DataFrame) -> None:
    """Create and display a bar chart for order status."""
    if df is not None and not df.empty:
        summary = df['受注の有無'].value_counts().reset_index()
        summary.columns = ['受注の有無', '件数']
        
        fig = px.bar(
            summary,
            x='受注の有無',
            y='件数',
            title='受注の有無別の件数',
            labels={'受注の有無': '', '件数': '件数'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def create_category_chart(df: pd.DataFrame, category: str) -> None:
    """Create and display a bar chart for the specified category."""
    if df is not None and not df.empty:
        summary = df[category].value_counts().reset_index()
        summary.columns = [category, '件数']
        
        fig = px.bar(
            summary,
            x=category,
            y='件数',
            title=f'{category}別の件数',
            labels={category: '', '件数': '件数'}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

def create_value_distribution_chart(df: pd.DataFrame, category: str, value_column: str) -> None:
    """Create and display a box plot for value distribution by category."""
    if df is not None and not df.empty and value_column in df.columns:
        fig = px.box(
            df,
            x=category,
            y=value_column,
            title=f'{category}別の{value_column}分布',
            labels={category: '', value_column: value_column}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="顧客情報分析", layout="wide")
    st.title("顧客情報分析システム")

    # File upload
    uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=['xlsx', 'xls'])

    if uploaded_file is not None:
        df = load_and_process_data(uploaded_file)
        
        if df is not None:
            # Section 1: Order Status Analysis
            st.header("1. 受注の有無分析")
            order_status = st.multiselect(
                "受注の有無を選択",
                options=[True, False],
                default=[True, False]
            )
            filtered_df = df[df['受注の有無'].isin(order_status)]
            create_order_status_chart(filtered_df)

            # Section 2: Category Analysis
            st.header("2. 業種分類分析")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_main_categories = st.multiselect(
                    "業種大分類を選択",
                    options=MAIN_CATEGORIES,
                    default=[]
                )
                if selected_main_categories:
                    filtered_df = filtered_df[filtered_df['業種大分類'].isin(selected_main_categories)]
                create_category_chart(filtered_df, '業種大分類')

            with col2:
                selected_sub_categories = st.multiselect(
                    "業種中分類を選択",
                    options=SUB_CATEGORIES,
                    default=[]
                )
                if selected_sub_categories:
                    filtered_df = filtered_df[filtered_df['業種中分類'].isin(selected_sub_categories)]
                create_category_chart(filtered_df, '業種中分類')

            # Section 3: Value Distribution Analysis
            st.header("3. 数値分布分析")
            col3, col4 = st.columns(2)
            
            with col3:
                if '汚泥濃度TS%' in df.columns:
                    st.subheader("汚泥濃度TS%の分布")
                    category_for_ts = st.selectbox(
                        "分類を選択 (汚泥濃度TS%)",
                        ['業種大分類', '業種中分類']
                    )
                    create_value_distribution_chart(filtered_df, category_for_ts, '汚泥濃度TS%')

            with col4:
                if '脱水ケーキ含水率％' in df.columns:
                    st.subheader("脱水ケーキ含水率％の分布")
                    category_for_moisture = st.selectbox(
                        "分類を選択 (脱水ケーキ含水率％)",
                        ['業種大分類', '業種中分類']
                    )
                    create_value_distribution_chart(filtered_df, category_for_moisture, '脱水ケーキ含水率％')

            # Display filtered data
            st.header("フィルター後のデータ")
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main() 
