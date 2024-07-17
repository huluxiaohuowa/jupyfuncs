import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
import io

def extract_text_from_image(
    image: Image.Image,
    lang: str = "eng"
) -> str:
    return pytesseract.image_to_string(image, lang=lang)

def extract_tables_from_pdf(
    pdf_path,
    lang="eng",
    table_from_pic: bool = False
):
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # 尝试提取表格
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df['Page'] = page_number + 1  # 添加页码信息
                    all_tables.append(df)
            if table_from_pic:
            # 提取页面中的图片并进行 OCR 识别
                for img in page.images:
                    try:
                        x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
                        # 检查边界
                        if x0 < 0 or top < 0 or x1 > page.width or bottom > page.height:
                            print(f"Skipping image with invalid bounds on page {page_number + 1}")
                            continue
                        
                        # 提取图像区域并转换为 PIL 图像
                        cropped_image = page.within_bbox((x0, top, x1, bottom)).to_image()
                        img_bytes = io.BytesIO()
                        cropped_image.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        pil_image = Image.open(img_bytes)
                        
                        # 进行 OCR 识别
                        ocr_text = extract_text_from_image(pil_image, lang=lang)
                        
                        # 假设 OCR 识别的文本是表格格式的（需要进一步处理和解析）
                        table = [line.split() for line in ocr_text.split('\n') if line.strip()]
                        
                        if table:
                            # 获取最大列数
                            num_columns = max(len(row) for row in table)
                            for row in table:
                                if len(row) != num_columns:
                                    row.extend([''] * (num_columns - len(row)))  # 补全缺失的列
                            
                            df = pd.DataFrame(table[1:], columns=table[0])
                            df['Page'] = page_number + 1  # 添加页码信息
                            all_tables.append(df)
                    except Exception as e:
                        print(f"Error processing image on page {page_number + 1}: {e}")
    
    if all_tables:
        return all_tables
    else:
        return [pd.DataFrame()] # 如果没有找到表格，返回空的 DataFrame


PROMPT_TABLE_SUM = """
你是负责总结表格和文本的助手，请不遗漏表格中的所有原始信息给出符合表格原始语言文字描述，并能准确找到行列对应关系，若表格中的文字没有具体语义含义，则不必进行过多推测或描述，给我一个空的字符串即可。表格或文本块：\n
"""

# def get_info_from_table()


# 示例调用
# pdf_path = pdf_path
# dfs = extract_tables_from_pdf(pdf_path, lang="chi_sim")