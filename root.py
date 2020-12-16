# --------------------------------------------------------------------------------------------------------------- #
# - This code was developed based on:                                                                           - #
# -                                                                                                             - #
# - "Tkinter Course - Create Graphic User - Interfaces in Python Tutorial" (accessed on 11/20/2020)             - #
# - available in: <https://www.youtube.com/watch?v=YXPyB4XeYLA&ab_channel=freeCodeCamp.org">                    - #
# -                                                                                                             - #
# - "Drag and Drop Images With The Mouse - Python Tkinter GUI Tutorial #71" (accessed on 11/25/2020)            - #
# - available in: <https://www.youtube.com/watch?v=Z4zePg2M5H8&ab_channel=Codemy.com>                           - #
# -                                                                                                             - #
# - StackOverflow Topic: "Python - Tkinter - Paint: How to Paint smoothly and save images with a                - #
# - different names?" (accessed on 12/01/2020) available in: <https://www.stackoverflow.com/questions/52146562> - #                                                    - #     
# -                                                                                                             - #
# - Default image by veronicataboada94 available in: <https://pixabay.com/pt/photos/...>                        - #   
# --------------------------------------------------------------------------------------------------------------- #


from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw
import os


# FUNCIONS ------------------------------------------------------------------------------------------------------ #
def open_images(): 
    global img_canvas, frame_img, files_path, images, images_marked, images_titles, draw

    files_path = filedialog.askopenfilenames(title = "Selecione as imagens", initialdir = r'C:\Users\henri\Desktop\manual_segmentation\input', filetypes = (('jpeg files', '*.jpg'),('png files', '*.png'),('tiff files', '*.tif')))
   
    images = []
    images_titles = []
    images_marked = []

    for item in files_path:
        head_tail = os.path.split(item)
        aux = head_tail[1].split('.')
        images_titles.append(aux[0])

        img = Image.open(item)

        [w_img, h_img] = img.size
        n = w_img/750
        w_img = int(w_img/n)
        h_img = int(h_img/n)

        img = img.resize((w_img, h_img), Image.BILINEAR)
        images.append(ImageTk.PhotoImage(img))

        img_blank = (Image.new("RGBA", (w_img, h_img), color=(255,255,255,255)))
        images_marked.append(img_blank)

    canvas_img.delete('all')
    img_canvas = canvas_img.create_image((w/2+2),(h/2+2), image = images[0])
    draw = ImageDraw.Draw(images_marked[0])

    if len(images) == 1:
        pass
    else:
        but_forward = Button(frame_tools, text = '>>', width = 7, command = lambda: forward_image(2))
        but_forward.grid(row = 0, column = 1, pady = 1)

    but_save = Button(frame_main, text = 'Salvar arquivo', width = 16, command = lambda: save_files(0))
    but_save.grid(row = 1, column = 0, pady = 1)

    image_number=1
    status_bar(image_number)

def save_files(image_number):
    filename = f'output\\marked_{images_titles[image_number]}.png'
    images_marked[image_number].save(filename)

def forward_image(image_number):
    global but_forward, but_back, img_canvas, back_image, draw

    canvas_img.delete('all')
    img_canvas = canvas_img.create_image(400,300,image = images[image_number-1])
    draw = ImageDraw.Draw(images_marked[image_number-1])

    but_forward = Button(frame_tools, text = '>>', width = 7, command = lambda: forward_image(image_number+1))
    but_back = Button(frame_tools, text = '<<', width = 7, command = lambda: back_image(image_number-1))

    if image_number == len(images):
        but_forward = Button(frame_tools, text = '>>', width = 7, state = DISABLED)

    but_back.grid(row = 0, column = 0, pady = 1)
    but_forward.grid(row = 0, column = 1, pady = 1)

    but_save = Button(frame_main, text = 'Salvar arquivo', width = 16, command = lambda: save_files(image_number-1))
    but_save.grid(row = 1, column = 0, pady = 1)

    status_bar(image_number)

def back_image(image_number):
    global but_forward, but_back, img_canvas, forward_image, draw

    canvas_img.delete('all')
    img_canvas = canvas_img.create_image(400, 300, image = images[image_number-1])
    draw = ImageDraw.Draw(images_marked[image_number-1])

    but_forward = Button(frame_tools, text = '>>', width = 7, command = lambda: forward_image(image_number+1))
    but_back = Button(frame_tools, text = '<<', width = 7, command = lambda: back_image(image_number-1))

    if image_number == 1:
        but_back = Button(frame_tools, text = '<<', width = 7, state = DISABLED)

    but_back.grid(row = 0, column = 0, pady = 1)
    but_forward.grid(row = 0, column = 1, pady = 1)

    but_save = Button(frame_main, text = 'Salvar arquivo', width = 16, command = lambda: save_files(image_number-1))
    but_save.grid(row = 1, column = 0, pady = 1)

    status_bar(image_number)

def status_bar(image_number):
    label_sts_bar_name = Label(root, text = ' Título da Imagem: {}'.format(images_titles[image_number-1]), bd=1, relief=SUNKEN, anchor = W)
    label_sts_bar_number = Label(root, text = ' Imagem {} de {}'.format(image_number, len(images)), bd=1, relief=SUNKEN, anchor = W)
    label_sts_bar_name.grid(row = 2, column = 0, columnspan = 2, sticky = W+E)
    label_sts_bar_number.grid(row = 2, column = 1, columnspan = 2, sticky = W+E)

def position(event):
    mouse_label.config(text = 'Posição do cursor\nx:' + str(event.x) + ', y:' + str(event.y))

def activate_mark(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y
    canvas_img.bind('<B1-Motion>', mark)

def mark(event):
    global lastx, lasty, draw, clicked

    color = {
        'Azul' : 'blue', 
        'Amarelo' : 'yellow', 
        'Vermelho' : 'red', 
        'Rosa' : 'pink'
    }

    position(event)

    x, y = event.x, event.y
    canvas_img.create_line((lastx, lasty, x, y), width = 5, fill = color[clicked.get()])
    draw.line((lastx, lasty, x, y), fill='black', width=5)
    lastx, lasty = x, y
# --------------------------------------------------------------------------------------------------------------- #


root = Tk()

root.title("SEGMENTAÇÃO MANUAL")
root.iconbitmap(r"utils\icon.ico")

#frame_image
frame_img = LabelFrame(root, text = 'image_frame', padx = 5, pady = 5)
frame_img.grid(row = 0, column = 0, padx = 5, pady = 5, rowspan=2)

#frame_main_buttons
frame_main = LabelFrame(root, text = 'main_buttons_frame', padx = 5, pady = 5)
frame_main.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = N)

#frame_tools_buttons
frame_tools = LabelFrame(root, text = 'tool_buttons_frame', padx = 5, pady = 5)
frame_tools.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = N)

#size
w = 800
h = 0.75 * w

#canvas_image
canvas_img = Canvas(frame_img, width=w, heigh=h, bg='green')
canvas_img.pack()

#images
img = ImageTk.PhotoImage(Image.open(r'utils\default_image.jpg'))
img_canvas = canvas_img.create_image((w/2+2),(h/2+2), image = img)

img_blank = Image.new("RGBA", (750, 498), color=(255,255,255,255))
draw = ImageDraw.Draw(img_blank)

#mark
lastx, lasty = None, None
canvas_img.bind('<Button-1>', activate_mark)

#main_buttons
but_open = Button(frame_main, text = 'Abrir imagens', width = 16, command = open_images)
but_save = Button(frame_main, text = 'Salvar arquivo', width = 16, state = DISABLED, command = save_files)
but_quit = Button(frame_main, text = 'Fechar', width = 16, command = root.quit)

but_open.grid(row = 0, column = 0, pady = 1) 
but_save.grid(row = 1, column = 0, pady = 1)
but_quit.grid(row = 2, column = 0, pady = 8)

#tool_buttons
but_back = Button(frame_tools, text = '<<', width = 7, state = DISABLED, command = back_image)
but_forward = Button(frame_tools, text = '>>', width = 7, state = DISABLED, command = lambda: forward_image(2))

clicked = StringVar()
clicked.set("Azul")
but_color = OptionMenu(frame_tools, clicked, 'Azul', 'Amarelo', 'Vermelho', 'Rosa')

mouse_label = Label(frame_tools, text='Posição do cursor\nx:    , y:    ')
canvas_img.bind('<Motion>', position)

but_back.grid(row = 0, column = 0, pady = 1)
but_forward.grid(row = 0, column = 1, pady = 1)
but_color.grid (row = 1, column = 0, pady = 1, columnspan = 2)
mouse_label.grid(row = 2, column = 0, pady = 1, columnspan = 2)

#status bar
label_sts_bar_name = Label(root, text = ' Título da Imagem: {}'.format("'Default Image' por veronicataboada94 disponível em <www.pixabay.com>"), bd=1, relief=SUNKEN, anchor = W)
label_sts_bar_number = Label(root, text = ' Imagem {} de {}'.format(0, 0), bd=1, relief=SUNKEN, anchor = W)
label_sts_bar_name.grid(row = 2, column = 0, columnspan = 2, sticky = W+E)
label_sts_bar_number.grid(row = 2, column = 1, columnspan = 2, sticky = W+E)


root.mainloop()