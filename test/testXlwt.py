import xlwt

workbook = xlwt.Workbook(encoding="utf-8")  # 创建对象
worksheet = workbook.add_sheet('sheet1')  # 添加一页sheet
worksheet.write(0, 0, 'hello')  # 向第一个单元写入数据
workbook.save('../outData/data.xls')  # 保存文件


