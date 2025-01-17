import random

import PyPDF2


class PDFReader:
    def __init__(self, pdf_path='Atomic_habits.pdf'):
        self.text_content = []
        
        # 读取PDF文件
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 遍历所有页面并提取文本
            for page in pdf_reader.pages:
                text = page.extract_text()
                # 按句子分割文本
                # 过滤空句子并存储
                self.text_content.append(text)
    
    def get_random_excerpt(self, target_length=100):
        # 随机选择一个句子
        sentence = random.choice(self.text_content)
        
        return sentence.strip().replace("\n", " ").replace("\t", " ")

# 使用示例
if __name__ == "__main__":
    pdf_reader = PDFReader()
    # 获取随机片段
    print(pdf_reader.get_random_excerpt())
