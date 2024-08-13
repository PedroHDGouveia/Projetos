import pyautogui
import time

def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
def check_screen():
    try:
        button_pos = pyautogui.locateOnScreen('imagem.formato', confidence=0.7)
        if button_pos is not None:
            time.sleep(1)
            click(button_pos.left, button_pos.top)
            return True
        else:
            return False
    except pyautogui.ImageNotFoundException:
        return False

def main():
    while True:
        if check_screen():
            print("Mensagem.")
            check_screen()
        else:
            print("Aguardando instrução...")
            time.sleep(1)

if __name__ == "__main__":
    main()
