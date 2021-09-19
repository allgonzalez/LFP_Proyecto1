
import imgkit
options = {
    'format': 'png',
    'crop-w': '430',
    'encoding': "UTF-8",
}
path_wkthmltoimage = r'C:\\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
imgkit.from_file('dibujo.html', 'ImagenOriginal.png', config=config, options=options)
