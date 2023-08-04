import matplotlib.pyplot as plt

# Reemplaza 'archivo.ods' con la ruta correcta de tu archivo .ods
ruta_archivo = 'TPL1_Mediciones.txt'

freq_mod= []
resp_mod = []
            
with open(ruta_archivo, 'r') as archivo_txt:
    lector_txt = archivo_txt.readlines()
    
    qty_rows_values = 22
    qty_rows_titles = 0
    qty_rows_blanks = 0
    qty_rows_freq_vs_freq = qty_rows_titles + qty_rows_values
    qty_rows_total = qty_rows_values + qty_rows_blanks + qty_rows_titles + qty_rows_values
    row_index = 0
    
    for row_freq_resp in lector_txt:
        #print('{}'.format(row_index))
        row_index += 1
        if ( row_index > ( qty_rows_freq_vs_freq + qty_rows_blanks + qty_rows_titles ) and row_index < qty_rows_total ):
            freq_mod_data, resp_mod_data, resp_mod_dB_data = row_freq_resp
            freq_mod.append(float(freq_mod_data))
            resp_mod.append(float(resp_mod_dB_data))

print(resp_mod)
#print('{}'.format(resp_mod))

"""
figura_1= plt.figure()
plt.plot(freq_mod, resp_mod)

plt.xscale('log')

plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Ganancia [dB]')

dresp= 10
plt.xlim(min(freq_mod), max(freq_mod))
plt.ylim(min(resp_mod), max(resp_mod)+dresp)

plt.grid(True, which= 'both')

plt.title('Respuesta en Frecuencia - Filtro Pasabajos')

plt.show()
"""