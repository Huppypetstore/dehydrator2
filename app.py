import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Dict

# 多言語テキスト辞書
TEXTS = {
    "title": {"ja": "\U0001F4CA 引き合い情報分析 APP", "en": "\U0001F4CA Dewatering Machine Inquiry Analysis APP"},
    "upload": {"ja": "Excelファイルをアップロードしてください", "en": "Please upload an Excel file"},
    "filter_settings": {"ja": "フィルター設定", "en": "Filter Settings"},
    "order_status": {"ja": "受注の有無", "en": "Order Status"},
    "main_category": {"ja": "業種大分類", "en": "Main Category"},
    "sub_category": {"ja": "業種中分類", "en": "Sub Category"},
    "machine_type": {"ja": "脱水機種別", "en": "Dewatering Machine Type"},
    "analysis_result": {"ja": "分析結果", "en": "Analysis Result"},
    "total_count": {"ja": "フィルター適用後の総件数", "en": "Total Count After Filtering"},
    "chart_type": {"ja": "グラフの種類を選択してください:", "en": "Select Chart Type:"},
    "numeric_analysis": {"ja": "数値分析（箱ひげ図と要約統計量）", "en": "Numeric Analysis (Boxplot & Summary Stats)"},
    "boxplot1": {"ja": "箱ひげ図 1：業種大分類", "en": "Boxplot 1: Main Category"},
    "boxplot2": {"ja": "箱ひげ図 2：業種中分類", "en": "Boxplot 2: Sub Category"},
    "select_numeric": {"ja": "数値項目を選択してください", "en": "Select Numeric Column"},
    "show_outliers": {"ja": "外れ値を表示", "en": "Show Outliers"},
    "show_zeros": {"ja": "0を表示", "en": "Show Zeros"},
    "summary_stats_main": {"ja": "\U0001F4CA {col} の要約統計量 (業種大分類別)", "en": "\U0001F4CA Summary Stats of {col} (by Main Category)"},
    "summary_stats_sub": {"ja": "\U0001F4CA {col} の要約統計量 (業種中分類別)", "en": "\U0001F4CA Summary Stats of {col} (by Sub Category)"},
    "filtered_data": {"ja": "フィルター後のデータ", "en": "Filtered Data"},
    "not_found": {"ja": "データに「{col}」列が見つかりませんでした。", "en": "Column '{col}' not found in data."},
    "not_found_chart": {"ja": "データに「{col}」列が見つかりませんでした。件数グラフは表示されません。", "en": "Column '{col}' not found in data. Count chart will not be displayed."},
    "not_found_box1": {"ja": "データに「業種大分類」列が見つからなかったため、箱ひげ図 1 は表示されません。", "en": "Column 'Main Category' not found. Boxplot 1 will not be displayed."},
    "not_found_box2": {"ja": "データに「業種中分類」列が見つからなかったため、箱ひげ図 2 は表示されません。", "en": "Column 'Sub Category' not found. Boxplot 2 will not be displayed."},
    "not_found_stats_main": {"ja": "データに「業種大分類」列が見つからなかったため、業種大分類別の要約統計量は表示されません。", "en": "Column 'Main Category' not found. Summary stats by Main Category will not be displayed."},
    "not_found_stats_sub": {"ja": "データに「業種中分類」列が見つからなかったため、業種中分類別の要約統計量は表示されません。", "en": "Column 'Sub Category' not found. Summary stats by Sub Category will not be displayed."},
    "not_found_numeric": {"ja": "箱ひげ図と要約統計量を作成できる数値項目が見つかりません。", "en": "No numeric columns found for boxplot and summary stats."},
    "lang_select": {"ja": "言語", "en": "Language"},
    "lang_ja": {"ja": "日本語", "en": "Japanese"},
    "lang_en": {"ja": "英語", "en": "English"},
}

# カテゴリも多言語化
MAIN_CATEGORIES = {
    "ja": [
        "エネルギー関連", "クリーニング工場", "下水関連",
        "化学製品工場", "化学薬品工場", "機械製造業", "産業廃棄物", "商業施設",
        "食品製造", "製紙", "繊維製品", "畜産", "発電所", "公共下水"
    ],
    "en": [
        "Energy-related", "Cleaning Factory", "Sewage-related",
        "Chemical Product Factory", "Chemical Plant", "Machinery Manufacturing", "Industrial Waste", "Commercial Facility",
        "Food Manufacturing", "Paper Manufacturing", "Textile Products", "Livestock", "Power Plant", "Public Sewage"
    ]
}

SUB_CATEGORIES = {
    "ja": [
        "ガラス", "ごみ処理施設", "シャーペンの芯製造工場", "ショッピングモール",
        "し尿処理場", "バイオガス", "バイオマス", "ビル", "ホテル",
        "メタン発酵残渣", "レジャー施設", "レンダリング", "移動脱水車", "飲料",
        "下水処理場", "化粧品", "外食", "学校", "給食センター", "漁業集落排水",
        "金属", "健康食品", "自動車・二輪", "樹脂", "浄化槽", "食肉加工",
        "食品加工", "食料品", "水産加工", "精米", "製パン", "製菓",
        "製麵", "製薬", "洗剤", "染料", "繊維・衣料", "繊維製品", "調味料",
        "漬物", "電気・電子部品", "電力", "塗装", "塗装系排水処理", "塗料",
        "肉牛", "乳牛（酪農）", "農業集落排水",
        "廃プラ", "プラ再生工場", "発電所", "病院", "薬品", "油田", "溶剤",
        "養鶏", "養豚", "冷凍・チルド・中食", "OD直脱"
    ],
    "en": [
        "Glass", "Waste Treatment Facility", "Mechanical Pencil Lead Factory", "Shopping Mall",
        "Night Soil Treatment Plant", "Biogas", "Biomass", "Building", "Hotel",
        "Methane Fermentation Residue", "Leisure Facility", "Rendering", "Mobile Dewatering Vehicle", "Beverage",
        "Sewage Treatment Plant", "Cosmetics", "Dining Out", "School", "School Lunch Center", "Fishing Village Sewage",
        "Metal", "Health Food", "Automobile/Motorcycle", "Resin", "Septic Tank", "Meat Processing",
        "Food Processing", "Foodstuffs", "Marine Product Processing", "Rice Polishing", "Bread Manufacturing", "Confectionery",
        "Noodle Manufacturing", "Pharmaceutical", "Detergent", "Dye", "Textile/Clothing", "Textile Products", "Seasoning",
        "Pickles", "Electric/Electronic Parts", "Electric Power", "Painting", "Painting Wastewater Treatment", "Paint",
        "Beef Cattle", "Dairy Cattle (Dairy Farming)", "Agricultural Village Sewage",
        "Waste Plastic", "Plastic Recycling Plant", "Power Plant", "Hospital", "Chemicals", "Oil Field", "Solvent",
        "Poultry", "Pig Farming", "Frozen/Chilled/Prepared Food", "OD Direct Dewatering"
    ]
}

DEWATERING_MACHINE_TYPES = {
    "ja": [
        "多重円板型脱水機", "多重板型スクリュープレス脱水機", "多重板型スクリュープレス脱水機小規模下水"
    ],
    "en": [
        "Multi-disc Dewatering Machine", "Multi-plate Screw Press Dewatering Machine", "Multi-plate Screw Press Dewatering Machine (Small-scale Sewage)"
    ]
}

def load_and_process_data(uploaded_file) -> pd.DataFrame:
    """Load and process the uploaded Excel file."""
    try:
        df = pd.read_excel(uploaded_file)

        # Data Cleaning: Convert non-numeric, empty strings, or whitespace to NaN for specific columns
        columns_to_clean = ['固形物回収率 %', '脱水ケーキ含水率 %']
        for col in columns_to_clean:
            if col in df.columns:
                # Convert all non-numeric values (including blank strings) to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Also replace any remaining whitespace-only strings with NaN
                df[col] = df[col].replace(r'^s*$', pd.NA, regex=True)

        return df
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return None

def create_boxplot(df: pd.DataFrame, value_col: str, category_col: str, show_outliers: bool = True, lang: str = "ja") -> None:
    """Create and display a boxplot for the specified value column, grouped by a specified category.
       Optionally hide outliers."""
    if df is not None and not df.empty:
        points_mode = 'all' if show_outliers else False
        fig = px.box(
            df,
            x=category_col,
            y=value_col,
            points=points_mode,
            title=f"{category_col}{'ごと' if lang=='ja' else ' by '}{value_col}{'の箱ひげ図' if lang=='ja' else ' Boxplot'}"
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

def create_summary_chart(df: pd.DataFrame, group_by: str, lang: str = "ja") -> None:
    """Create and display a bar chart for the specified grouping (count)."""
    if df is not None and not df.empty:
        # Group by the primary category and then by '脱水機種別' for color splitting
        if group_by in [TEXTS["main_category"][lang], TEXTS["sub_category"][lang]]:
            # Use the dataframe filtered by user selections in main directly
            df_to_chart = df

            # Group the filtered dataframe
            # Ensure '脱水機種別' column exists before grouping
            if TEXTS["machine_type"][lang] in df_to_chart.columns:
                 summary = df_to_chart.groupby([group_by, TEXTS["machine_type"][lang]]).size().reset_index(name='件数')
                 # Sort by primary group and then by count for stacking order
                 summary = summary.sort_values(by=[group_by, '件数'], ascending=[True, False])
                 color_col = TEXTS["machine_type"][lang]
            else:
                 # Fallback if '脱水機種別' column is missing in the filtered data
                 summary = df_to_chart.groupby([group_by]).size().reset_index(name='件数')
                 color_col = None


        else:
            summary = df[group_by].value_counts().reset_index()
            summary.columns = [group_by, '件数']
            color_col = None # No color grouping for other chart types

        # Calculate total counts for sorting x-axis categories
        # Use the original df for sorting to get all categories, or the summary df if only filtered categories are desired
        # Using summary df for sorting categories present in the current view
        if group_by in summary.columns:
             total_counts = summary.groupby(group_by)['件数'].sum().reset_index()
             sorted_categories = total_counts.sort_values('件数', ascending=False)[group_by].tolist()
        else:
             # Fallback sorting if group_by column is not directly in summary (e.g., if no data after filtering)
             sorted_categories = summary[group_by].tolist() if group_by in summary.columns else []


        fig = px.bar(
            summary,
            x=group_by,
            y='件数',
            title=f'{group_by}{"別の件数" if lang=="ja" else " Count by " + group_by}',
            labels={group_by: '', '件数': '件数' if lang=="ja" else 'Count'},
            color=color_col, # Apply color grouping
            text='件数', # Use the '件数' column for text labels
            text_auto=True, # Automatically position text labels
            color_discrete_sequence=px.colors.qualitative.Pastel, # Use a pastel color sequence
            category_orders={group_by: sorted_categories} # Apply sorting to x-axis categories
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    # 言語選択
    lang = st.sidebar.selectbox(
        TEXTS["lang_select"]["ja"] + " / " + TEXTS["lang_select"]["en"],
        options=["ja", "en"],
        format_func=lambda x: TEXTS["lang_ja"]["ja"] if x=="ja" else TEXTS["lang_en"]["ja"]
    )
    st.set_page_config(page_title=TEXTS["title"][lang], layout="wide")
    st.title(TEXTS["title"][lang])

    # ファイルアップロード
    uploaded_file = st.file_uploader(TEXTS["upload"][lang], type=['xlsx', 'xls'])

    if uploaded_file is not None:
        df = load_and_process_data(uploaded_file)

        if df is not None:
            # フィルター設定
            st.header(TEXTS["filter_settings"][lang])
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                order_status = st.multiselect(
                    TEXTS["order_status"][lang],
                    options=[True, False],
                    default=[True, False]
                )
            with col2:
                # Use predefined list for options
                selected_main_categories = st.multiselect(
                    TEXTS["main_category"][lang],
                    options=sorted(MAIN_CATEGORIES[lang]), # Use the constant list directly
                    default=[]
                )
            with col3:
                # Use predefined list for options
                selected_sub_categories = st.multiselect(
                    TEXTS["sub_category"][lang],
                    options=sorted(SUB_CATEGORIES[lang]), # Use the constant list directly
                    default=[]
                )
            with col4:
                selected_machine_types = st.multiselect(
                    TEXTS["machine_type"][lang],
                    options=DEWATERING_MACHINE_TYPES[lang],
                    default=[]
                )

            filtered_df = df.copy()
            if order_status:
                filtered_df = filtered_df[filtered_df[TEXTS["order_status"][lang]].isin(order_status)] if TEXTS["order_status"][lang] in filtered_df.columns else filtered_df
            if selected_main_categories:
                # Ensure the column exists before filtering
                if TEXTS["main_category"][lang] in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[TEXTS["main_category"][lang]].isin(selected_main_categories)]
                else:
                    st.warning(TEXTS["not_found"].get(lang, "").format(col=TEXTS["main_category"][lang]))
                    filtered_df = filtered_df[filtered_df[TEXTS["main_category"][lang]].isnull()] # Filter out everything


            if selected_sub_categories:
                # Ensure the column exists before filtering
                if TEXTS["sub_category"][lang] in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[TEXTS["sub_category"][lang]].isin(selected_sub_categories)]
                else:
                    st.warning(TEXTS["not_found"].get(lang, "").format(col=TEXTS["sub_category"][lang]))
                    filtered_df = filtered_df[filtered_df[TEXTS["sub_category"][lang]].isnull()] # Filter out everything


            if selected_machine_types and TEXTS["machine_type"][lang] in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[TEXTS["machine_type"][lang]].isin(selected_machine_types)]
            # Add handling for when '脱水機種別' column is missing but a selection was made
            elif selected_machine_types and TEXTS["machine_type"][lang] not in filtered_df.columns:
                 st.warning(TEXTS["not_found"].get(lang, "").format(col=TEXTS["machine_type"][lang]))
                 # In this case, the filter is effectively ignored, no need to modify filtered_df


            # 分析結果（件数）
            st.header(TEXTS["analysis_result"][lang])
            st.write(f"{TEXTS['total_count'][lang]}: {len(filtered_df)}")

            st.subheader("件数グラフ" if lang=="ja" else "Count Chart")
            chart_type_options = [TEXTS["main_category"][lang], TEXTS["sub_category"][lang], TEXTS["order_status"][lang]]
            chart_type = st.radio(
                TEXTS["chart_type"][lang],
                chart_type_options
            )
            # Ensure the selected chart_type column exists in the dataframe before charting
            if chart_type in filtered_df.columns:
                create_summary_chart(filtered_df, chart_type, lang)
            else:
                st.warning(TEXTS["not_found_chart"][lang].format(col=chart_type))


            # 数値分析（箱ひげ図と要約統計量）
            st.header(TEXTS["numeric_analysis"][lang])
            # Use the filtered dataframe to get numeric columns
            numeric_columns = filtered_df.select_dtypes(include='number').columns.tolist()

            # --- Add print statements for debugging ---
            print("Original DataFrame columns:", df.columns.tolist())
            print("Filtered DataFrame columns:", filtered_df.columns.tolist())
            print("Numeric columns found:", numeric_columns)
            # --- End print statements ---

            # Define the preferred order of columns
            preferred_columns = ["汚泥濃度 TS%", "VTS%/TS", "脱水ケーキ含水率 %", "固形物回収率 %"]

            # Create the ordered list for selectbox options
            # Start with preferred columns that are present in numeric_columns
            ordered_numeric_columns = [col for col in preferred_columns if col in numeric_columns]

            # Add the remaining numeric columns that are not in the preferred list, maintaining their original relative order
            ordered_numeric_columns.extend([col for col in numeric_columns if col not in preferred_columns])


            # Initialize selected value variables
            value_col_main = None
            value_col_sub = None

            if ordered_numeric_columns:
                # 2つの列を作成して箱ひげ図と要約統計量を並列配置
                col_box1, col_box2 = st.columns(2)

                with col_box1:
                    # 箱ひげ図 1：業種大分類 ごと
                    st.subheader(TEXTS["boxplot1"][lang])
                    # Use the ordered list for options
                    value_col_main = st.selectbox(TEXTS["select_numeric"][lang], ordered_numeric_columns, key="boxplot1_value")
                    show_outliers_main = st.checkbox(TEXTS["show_outliers"][lang], value=False, key="outliers_main")
                    show_zeros_main = st.checkbox(TEXTS["show_zeros"][lang], value=False, key="show_zeros_main")
                    # Ensure '業種大分類' column exists before creating the boxplot
                    if TEXTS["main_category"][lang] in filtered_df.columns:
                        if value_col_main:
                            # Filter out 0 and NaN values for specific columns if selected
                            df_for_analysis_main = filtered_df.copy()
                            columns_to_filter_zero_and_nan = ['固形物回収率 %', '脱水ケーキ含水率 %']
                            if value_col_main in columns_to_filter_zero_and_nan and not show_zeros_main:
                                df_for_analysis_main = df_for_analysis_main[df_for_analysis_main[value_col_main].notna() & (df_for_analysis_main[value_col_main] != 0)]
                            elif value_col_main in columns_to_filter_zero_and_nan and show_zeros_main:
                                df_for_analysis_main = df_for_analysis_main[df_for_analysis_main[value_col_main].notna()] # Just filter NaNs if show_zeros is true


                            # Sort categories by count for boxplot
                            # Use the filtered dataframe for counts to reflect the current view
                            category_counts_main = df_for_analysis_main[TEXTS["main_category"][lang]].value_counts().reset_index()
                            category_counts_main.columns = [TEXTS["main_category"][lang], 'count']
                            sorted_categories_main = category_counts_main.sort_values('count', ascending=False)[TEXTS["main_category"][lang]].tolist()

                            # Create boxplot with sorted categories
                            fig_main = px.box(
                                df_for_analysis_main,
                                x=TEXTS["main_category"][lang],
                                y=value_col_main,
                                points='all' if show_outliers_main else False,
                                title=f"{TEXTS['main_category'][lang]}{'ごと' if lang=='ja' else ' by '}{value_col_main}{'の箱ひげ図' if lang=='ja' else ' Boxplot'}",
                                category_orders={TEXTS["main_category"][lang]: sorted_categories_main}
                            )
                            fig_main.update_layout(
                                xaxis_tickangle=-45,
                                height=600
                            )
                            st.plotly_chart(fig_main, use_container_width=True, config={'scrollZoom': True})

                            st.markdown("---") # 区切り線を追加

                            # 要約統計量：業種大分類ごと
                            st.subheader(TEXTS["summary_stats_main"][lang].format(col=value_col_main))
                            try:
                                # Ensure the column exists before grouping
                                if TEXTS["main_category"][lang] in df_for_analysis_main.columns:
                                     grouped_stats_main = df_for_analysis_main.groupby(TEXTS["main_category"][lang])[value_col_main].describe()
                                     st.dataframe(grouped_stats_main)
                                else:
                                     st.warning(TEXTS["not_found_stats_main"][lang])

                            except Exception as e:
                                st.error(f"{TEXTS['main_category'][lang]}: {str(e)}")
                    else:
                         st.warning(TEXTS["not_found_box1"][lang])


                with col_box2:
                    # 箱ひげ図 2：業種中分類 ごと
                    st.subheader(TEXTS["boxplot2"][lang])
                    # Use the ordered list for options
                    value_col_sub = st.selectbox(TEXTS["select_numeric"][lang], ordered_numeric_columns, key="boxplot2_value")
                    show_outliers_sub = st.checkbox(TEXTS["show_outliers"][lang], value=False, key="outliers_sub")
                    show_zeros_sub = st.checkbox(TEXTS["show_zeros"][lang], value=False, key="show_zeros_sub")
                    # Ensure '業種中分類' column exists before creating the boxplot
                    if TEXTS["sub_category"][lang] in filtered_df.columns:
                        if value_col_sub:
                            # Filter out 0 and NaN values for specific columns if selected
                            df_for_analysis_sub = filtered_df.copy()
                            columns_to_filter_zero_and_nan = ['固形物回収率 %', '脱水ケーキ含水率 %']
                            if value_col_sub in columns_to_filter_zero_and_nan and not show_zeros_sub:
                                df_for_analysis_sub = df_for_analysis_sub[df_for_analysis_sub[value_col_sub].notna() & (df_for_analysis_sub[value_col_sub] != 0)]
                            elif value_col_sub in columns_to_filter_zero_and_nan and show_zeros_sub:
                                df_for_analysis_sub = df_for_analysis_sub[df_for_analysis_sub[value_col_sub].notna()] # Just filter NaNs if show_zeros is true


                            # Sort categories by count for boxplot
                            # Use the filtered dataframe for counts to reflect the current view
                            category_counts_sub = df_for_analysis_sub[TEXTS["sub_category"][lang]].value_counts().reset_index()
                            category_counts_sub.columns = [TEXTS["sub_category"][lang], 'count']
                            sorted_categories_sub = category_counts_sub.sort_values('count', ascending=False)[TEXTS["sub_category"][lang]].tolist()


                            # Create boxplot with sorted categories
                            fig_sub = px.box(
                                df_for_analysis_sub,
                                x=TEXTS["sub_category"][lang],
                                y=value_col_sub,
                                points='all' if show_outliers_sub else False,
                                title=f"{TEXTS['sub_category'][lang]}{'ごと' if lang=='ja' else ' by '}{value_col_sub}{'の箱ひげ図' if lang=='ja' else ' Boxplot'}",
                                category_orders={TEXTS["sub_category"][lang]: sorted_categories_sub}
                            )
                            fig_sub.update_layout(
                                xaxis_tickangle=-45,
                                height=600
                            )
                            st.plotly_chart(fig_sub, use_container_width=True, config={'scrollZoom': True})

                            st.markdown("---") # 区切り線を追加

                            # 要約統計量：業種中分類ごと
                            st.subheader(TEXTS["summary_stats_sub"][lang].format(col=value_col_sub))
                            try:
                                # Ensure the column exists before grouping
                                if TEXTS["sub_category"][lang] in df_for_analysis_sub.columns:
                                     grouped_stats_sub = df_for_analysis_sub.groupby(TEXTS["sub_category"][lang])[value_col_sub].describe()
                                     st.dataframe(grouped_stats_sub)
                                else:
                                     st.warning(TEXTS["not_found_stats_sub"][lang])

                            except Exception as e:
                                st.error(f"{TEXTS['sub_category'][lang]}: {str(e)}")
                    else:
                         st.warning(TEXTS["not_found_box2"][lang])


            else:
                st.warning(TEXTS["not_found_numeric"][lang])

            # フィルター後のデータ
            st.header(TEXTS["filtered_data"][lang])
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
