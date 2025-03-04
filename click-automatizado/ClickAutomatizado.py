import pyautogui
from time import sleep

def click(x, y):

    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()

def check_screen(image_path, confidence=0.7):

    try:
        button_pos = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if button_pos is not None:
            x, y = pyautogui.center(button_pos)
            click(x, y)
            print(f"Imagem encontrada e clicada em ({x}, {y}).")
            return True
    except pyautogui.ImageNotFoundException:
        print("Imagem não encontrada. Tentando novamente...")
    except Exception as e:
        print(f"Erro inesperado ao procurar a imagem: {e}")

    return False

def main():

    image_path = "imagem.png"
    max_attempts = 60
    delay_between_attempts = 1

    print("Iniciando a busca pela imagem...")
    for attempt in range(1, max_attempts + 1):
        print(f"Tentativa {attempt} de {max_attempts}...")
        if check_screen(image_path):
            print("Partida aceita com sucesso!")
            break
        sleep(delay_between_attempts)  
    else:
        print("Número máximo de tentativas alcançado. A imagem não foi encontrada.")

if __name__ == "__main__":
    main()