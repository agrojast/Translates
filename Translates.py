from Screenshot import Screenshot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

# Instancia única del navegador
driver = webdriver.Chrome()
#Maximizar la pantalla
driver.maximize_window()
ob = Screenshot.Screenshot()

#Ingresar a la TBX
def login(url, user, contraseña, app):
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    #Ingresar usuario
    username = wait.until(EC.presence_of_element_located((By.ID, 'mat-input-0')))
    username.send_keys(user)

    #Ingresar contraseña
    password = wait.until(EC.presence_of_element_located((By.ID, 'mat-input-1')))
    password.send_keys(contraseña)

    #Dar clic en botón login
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button__label')))
    button.click()

    #Dar clic en appdrawer
    appdrawer = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'apps')]")))
    appdrawer.click()

    #Seleccionar aplicación
    application = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '" + app + "')]")))
    application.click()

#Seleccionar un módulo
def select_module(modulo):
    wait = WebDriverWait(driver, 50)
    #La siguiente linea sirve para que primero pase el elemento y lo haga invisible y se pueda ver el segundo
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'loader ng-tns-c4059369084-0 ng-trigger ng-trigger-fadeIn')))

    module = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '" + modulo + "')]")))
    module.click()

#Abrir sección "My account"
def translate_open(Language):
    wait = WebDriverWait(driver, 50)
    admin = driver.find_element(By.CLASS_NAME, 'toolbar__user')
    admin.click()

    select_idioma = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '" + Language + "')]")))
     # Hacer clic en el elemento utilizando JavaScript
    driver.execute_script("arguments[0].click();", select_idioma)

#Seleccionar idioma
def select_language(culture):
    wait = WebDriverWait(driver, 60)
    language = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='"+ culture +"']")))    
    language.click()

#Validar traducción
def validate_translation(expected_text, screenshot_name, idioma):
    
    try:
        #Busca la traducción correspondiente
        driver.find_element(By.XPATH, f"//*[normalize-space(text())='{expected_text}']")
    
        # Eliminar el archivo existente si existe
        if os.path.exists(f"./img/{screenshot_name}.png"):
            os.remove(f"./img/{screenshot_name}.png")

        #Tomar pantallazo de toda la página
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        img_url = ob.full_screenshot(driver, save_path='./img', image_name=f'{screenshot_name}.png', is_load_at_runtime=True, load_wait_time=10)
        print(img_url)        
    except:
        #Sino encuentra la traducción manda esta excepción
        print(f"La traducción '{expected_text}' no está correcta en el idioma {idioma}.")
        raise Exception(f"Error de traducción en idioma {idioma}")

#Cerrar sección "My account"
def translate_close():
    wait = WebDriverWait(driver, 60)
    close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'toolbar__user')))
    close.click()

#Función principal
def main():
    try:
        wait = WebDriverWait(driver, 60)
        #Llamado de función login
        login('url','Username','Password', 'disruption')
        driver.implicitly_wait(5)

        #Seleccionar módulo
        select_module('Disruptions')        

        #Validar traducción en inglés
        validate_translation('Disruptions', 'Inglés', 'Inglés')

        #Validar traducción en armenio
        translate_open('Language ')
        select_language('Հայերեն (hy-AM)')
        translate_close()     
        validate_translation('Խափանումներ', 'Armenio', 'Armenio')

        #Validar traducción en chino
        translate_open('Լեզու ')
        select_language('中國人 (zh-CHT)')
        translate_close()     
        validate_translation('中断', 'Chino', 'Chino')

        #Validar traducción en francés
        translate_open('语 ')
        select_language('Français (fr-FR)')
        translate_close()     
        validate_translation('Perturbations', 'Francés', 'Francés')

        #Validar traducción en español
        translate_open('Langue ')
        select_language('Español (es-CO)')
        translate_close()     
        validate_translation('Disrupciones', 'Español', 'Español')  
              
        #Validar traducción en ruso
        translate_open('Idioma ')
        select_language('Русский (ru-RU)')
        translate_close()     
        validate_translation('Нарушения', 'Ruso', 'Ruso')

        #Validar traducción en rumano
        translate_open('Язык ')
        select_language('Română (ro-RO)')
        translate_close()     
        validate_translation('Perturbări', 'Rumano', 'Rumano')

        #Validar traducción en hindi
        translate_open('Limba ')
        select_language('हिन्दी (hi-HI)')
        translate_close()     
        validate_translation('अवरोधों', 'Hindi', 'Hindi')

        #Idioma default
        translate_open('भाषा ')
        select_language('English (en-US)')
        translate_close()

    finally:
        #Cerrar navegador y sesión
        driver.close()
        driver.quit()

if __name__ == "__main__":
    main()
