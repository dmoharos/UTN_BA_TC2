#-----------------------------------------------------------------------------------------------------------------------#

import csv
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------------------------------------------------#

ruta_archivo = 'TPL1_Respuesta_modulo_analizador.csv'

freq_mod= []
resp_mod = []

with open(ruta_archivo, 'r') as archivo_csv:
    lector_csv = csv.reader(archivo_csv)
    
    qty_rows_values = 100
    qty_rows_titles = 3
    qty_rows_blanks = 1
    
    qty_rows_freq_vs_freq = qty_rows_titles + qty_rows_values
    qty_rows_mod_vs_freq = qty_rows_titles + qty_rows_values
    qty_rows_total = qty_rows_freq_vs_freq + qty_rows_blanks + qty_rows_mod_vs_freq
    row_index = 0
    
    for row_freq_resp in lector_csv:
        #print('{}'.format(row_index))
        row_index += 1
        if ( row_index > ( qty_rows_freq_vs_freq + qty_rows_blanks + qty_rows_titles ) and row_index <= qty_rows_total ):
            freq_mod_data, resp_mod_data = row_freq_resp
            freq_mod.append(float(freq_mod_data))
            resp_mod.append(float(resp_mod_data))
            
print(resp_mod)

figura_1= plt.figure()
plt.plot(freq_mod, resp_mod)

plt.xscale('log')

plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Ganancia [dB]')

dresp= 0.5
plt.xlim(min(freq_mod), max(freq_mod))
plt.ylim(min(resp_mod), max(resp_mod)+dresp)

plt.grid(True, which= 'both')

plt.title('Respuesta en Frecuencia - Filtro Pasa Altos')

plt.show()


#-----------------------------------------------------------------------------------------------------------------------#

ruta_archivo = 'TPL1_Respuesta_fase_analizador.csv'

freq_fase = []
resp_fase_ch1 = []

with open(ruta_archivo, 'r') as archivo_csv:
    lector_csv = csv.reader(archivo_csv)
    
    qty_rows_values = 100
    qty_rows_titles = 3
    qty_rows_blanks = 1
    qty_rows_freq_vs_freq = qty_rows_titles + qty_rows_values
    qty_rows_phase_vs_freq = qty_rows_titles + qty_rows_values
    qty_rows_total = qty_rows_freq_vs_freq + qty_rows_blanks + qty_rows_phase_vs_freq
    row_index = 0
    
    for row_freq_resp_fase in lector_csv:
        #print('{}'.format(row_index))
        row_index += 1
        if ( row_index > ( qty_rows_freq_vs_freq + qty_rows_blanks + qty_rows_titles ) and row_index <= qty_rows_total ):
            freq_fase_data, resp_fase_ch1_data= row_freq_resp_fase
            freq_fase.append(float(freq_fase_data))
            resp_fase_ch1.append(float(resp_fase_ch1_data))

figura_1= plt.figure()
plt.plot(freq_fase, resp_fase_ch1)

plt.xscale('log')

plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Fase [º]')

dresp= 10
plt.xlim(min(freq_fase), max(freq_fase))
plt.ylim(min(resp_fase_ch1)-dresp, max(resp_fase_ch1)+dresp)

plt.grid(True, which= 'both')

plt.title('Respuesta de Fase - Filtro Pasa Altos')

plt.show()

#-----------------------------------------------------------------------------------------------------------------------#
