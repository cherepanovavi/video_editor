import sys
import argparse
import gui

help_str = 'Данное приложение реализует некоторые простые функции редактирования видео (mp4) файлов:' \
            '- чтобы обрезать фрагмент, выберите фрагмент из панели Video, нажмите CUT, и выберите начало ' \
           'и конец отрезка\n' \
            '- чтобы соединить два фрагмента выберите тот, который будет идти первым, из панели Video, нажмите\n' \
           'CONCAT и выберите второй фрагмент в предложенном списке\n' \
           '- чтобы добавить изображение, загрузите .jpg или .png файл через меню: File -> Import image, \n ' \
           'выберите видео на вкладке Video, выберите изображение на вкладке Images и нажмите ADD IMAGE '


def create_parser():
    parser = argparse.ArgumentParser(
        description=help_str
    )
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if len(sys.argv) == 1:
        gui.main()
