# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 11:28:34 2016

@author: ruiz
"""
import gdal
import numpy as np
import os
import h5py

class Converter_rasters_to_HDF5:
    '''
    #Pasta com os rasters
    >>>caminho='/media/Rasters'
    >>>arquivo_HDF5='/media/dados_hdf.hdf5'
    #foramto dos rasters
    >>>formato = '.tif'    
    #Obter nomes dos rasters
    >>>proc=Converter_rasters_to_HDF5(caminho, formato)
    #obter os caminhos e os nomes dos rasters
    >>>proc.obterNomesRasters()
    #Converter cada raster para HDF5
    >>>f_hdf=proc.Converte_Rasters_to_HDF(arquivo_HDF5)
        
    >>> f_hdf.close()
    '''
    
    def __init__(self,caminho, foramto):
        self.caminho=caminho
        self.formato=formato

        
    def obterNomesRasters(self):
        #armazena o caminho e o nome do raster
        self.caminho_nome_rasters = [[os.path.join(self.caminho,f),os.path.join(self.caminho,f).split('/')[-1].split('.')[0]] for f in os.listdir(self.caminho) if f.endswith(self.formato)]
        print self.caminho_nome_rasters
    
    def Converte_Rasters_to_HDF(self,arquivo_HDF):
        
        '''
        #Cria um HDF5 a partir das imagens na pasta
        '''
        #criar varuavel HDf
        self.arquivo_HDF=arquivo_HDF
        #criar arquivo HDF
        f_hdf = h5py.File(self.arquivo_HDF, "w",libver='latest')
        #percorrer cada raster e armazenar no HDF5
        for caminho, nome in self.caminho_nome_rasters:
            print 'Nomes rasters: ',nome
            #Obter drives para todos os tipos de imagem
            gdal.AllRegister()
            #Get metadata image
            ds = gdal.Open(caminho, gdal.GA_ReadOnly)
            #Total de colunas e linhas
            colunas= ds.RasterXSize
            linhas = ds.RasterYSize
            #Criar conjunto de dados HDF
            conjunto_dados = f_hdf.create_dataset(nome, (linhas,colunas), chunks=True,dtype=np.float32)#(linhas,1)
            #percorrer cada linha da imageme  armazenar no HDF
            for i in xrange(linhas):
                #Read segmentation how array
                conjunto_dados[i,:]=ds.GetRasterBand(1).ReadAsArray(0,i,colunas,1)
        return f_hdf
        
        
#Pasta com os rasters
caminho='/media/ruiz/Documentos/Pesquisas/Cicatrizes_Eduardo/Raster'
arquivo_HDF5='/media/ruiz/Documentos/Pesquisas/Cicatrizes_Eduardo/dados7.hdf5'
#foramto dos rasters
formato = '.tif'    
#Obter nomes dos rasters
proc=Converter_rasters_to_HDF5(caminho, formato)
#obter os caminhos e os nomes dos rasters
proc.obterNomesRasters()
#Converter cada raster para HDF5
f_hdf=proc.Converte_Rasters_to_HDF(arquivo_HDF5)
