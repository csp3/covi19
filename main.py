from flask import Flask, render_template, request, jsonify 
import time, os, shutil, re, openpyxl 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions 
from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

url = "https://app.powerbi.com/view?r=eyJrIjoiYzIzZThiNTYtYjUwMy00ZDVhLThhZjMtOWMyMzJhYTMzMjQ1IiwidCI6IjM0MGJjMDE2LWM2YTYtNDI2Ni05NGVjLWE3NDY0YmY5ZWM3MCIsImMiOjR9"

options = webdriver.ChromeOptions() 
options.headless = True
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options) 

driver.get(url)

ruta = r'C:\\Users\\casa\\Downloads\\' 
reg = r'CASOS_[\w\s]*2021[\w\s(\d)]*.xlsx'
regex = re.compile(reg)
lista_file = []
lista_modi = []
mifile = ''
lista_region = []
lista_pcr = []
lista_prapida = []
lista_pantigeno = []
lista_total = []
lista_fallecidos = []
lista = []

time.sleep(5)

@app.route("/", methods= ["POST"])
def listar():
    #data = request.form.getlist('valores[]') 

    try:
        butt = '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[28]/transform/div/div[3]/div/visual-modern/div/div'
        
        # descargando archivo 
        action = ActionChains(driver)
        ele = driver.find_element_by_xpath(butt)
        action.click(ele).perform()

        #copiando archivo 
        for f in os.listdir(ruta):
            if regex.search(f):
                lista_modi.append(os.stat(ruta+f)[9]) # [9] es st_ctime 

        lista_modi.sort(reverse = True)

        for f in os.listdir(ruta):
            if os.stat(ruta+f)[9] == lista_modi[0]:
                mifile = f
                break 
        try:
            shutil.copyfile(ruta + mifile, mifile)
            # shutil.move(ruta + mifile, mifile)
        except:
            print('Archivo abierto o no se pudo copiar')
            exit() 
        
        #obteniendo datos del excel
        excel = openpyxl.load_workbook(mifile)
        nombre_hoja = excel.get_sheet_names()[0]
        hoja = excel.get_sheet_by_name(nombre_hoja)
        lista_region = []
        lista_pcr = []
        lista_prapida = []
        lista_pantigeno = []
        lista_total = []
        lista_fallecidos = []
        lista = [] 
        for i in range(0, 25 + 1):
            celda = 'B' + str(i+2)
            lista_region.append(hoja[celda].value)
            celda = 'C' + str(i+2)
            lista_pcr.append(hoja[celda].value)
            celda = 'D' + str(i+2)
            lista_prapida.append(hoja[celda].value)
            celda = 'E' + str(i+2)
            lista_pantigeno.append(hoja[celda].value)
            celda = 'F' + str(i+2)
            lista_total.append(hoja[celda].value)
            celda = 'G' + str(i+2)
            lista_fallecidos.append(hoja[celda].value) 
        
        lista.append(lista_region)
        lista.append(lista_pcr)
        lista.append(lista_prapida)
        lista.append(lista_pantigeno)
        lista.append(lista_total)
        lista.append(lista_fallecidos)
    except Exception as e:
        print("exepcion") 

    # finally:
    #     driver.close()

    return jsonify(lista)

#MAIN
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=8089)
