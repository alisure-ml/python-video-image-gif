from ToolGif import ToolGif as tg
from ToolGif import SortGif as sg

if __name__ == "__main__":

    img_dir = "img/"
    gif_dir = "gif/test_main.gif"

    tg(img_dir, gif_dir, sort=sg.compare_filename, duration=0.2)

    pass
