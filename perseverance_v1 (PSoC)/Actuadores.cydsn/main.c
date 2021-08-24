/* ========================================
 *
 * Copyright JAIRO MAY, 2020
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF jairo may díaz.
 *
 * ========================================
*/
#include "project.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

////////////variables pata datos UART///////////////////
char strings[25];
char dato;
char imp[99];
const char split[]=",";
char *partes;
int d=0;
int control;
int n=0;
int k;

/////////////////////variables para motores/////////
volatile int pwm = 0;

/////////////////////variables para comunicacion/////////
volatile int cod1 = 0;
volatile int cod2 = 0;
char soy[20]="";
//////////////////////////////////////////////////////////

CY_ISR(UART_handler){
    
    dato = UART_GetChar();
    strings[n]=dato;
    
    if(dato != '#' && dato != '%'){n++;}
    
    if(dato=='#'){
        
        partes = strtok(strings, split);
        
        while(partes != NULL){
            control++;
            if(control == 1){
                pwm = atoi(partes);
            }
            else if(control == 2){
                d = atoi(partes);
                switch(d){
            case 1:
                //"Derecha"
                //M1
                EA1_Write(1);
                EB1_Write(0);
                //M2
                EA2_Write(0);
                EB2_Write(1);
                //M3
                EA3_Write(0);
                EB3_Write(1);
                //M4
                EA4_Write(1);
                EB4_Write(0);
                break;
            case 2:
                //NorDerecha
                //M1
                EA1_Write(1);
                EB1_Write(0);
                //M2
                EA2_Write(0);
                EB2_Write(0);
                //M3
                EA3_Write(0);
                EB3_Write(0);
                //M4
                EA4_Write(1);
                EB4_Write(0);
                break;
            case 3:
                //sprintf(direc,"Frente");
                //M1
                EA1_Write(1);
                EB1_Write(0);
                //M2
                EA2_Write(1);
                EB2_Write(0);
                //M3
                EA3_Write(1);
                EB3_Write(0);
                //M4
                EA4_Write(1);
                EB4_Write(0);
                break;
            case 4:
                //sprintf(direc,"NorIzquierda");
                //M1
                EA1_Write(0);
                EB1_Write(0);
                //M2
                EA2_Write(1);
                EB2_Write(0);
                //M3
                EA3_Write(1);
                EB3_Write(0);
                //M4
                EA4_Write(0);
                EB4_Write(0);
                break;
            case 5:
                //sprintf(direc,"Izquierda");
                //M1
                EA1_Write(0);
                EB1_Write(1);
                //M2
                EA2_Write(1);
                EB2_Write(0);
                //M3
                EA3_Write(1);
                EB3_Write(0);
                //M4
                EA4_Write(0);
                EB4_Write(1);
                break;
            case 6:
                //sprintf(direc,"SurIzquierda");
                //M1
                EA1_Write(0);
                EB1_Write(1);
                //M2
                EA2_Write(0);
                EB2_Write(0);
                //M3
                EA3_Write(0);
                EB3_Write(0);
                //M4
                EA4_Write(0);
                EB4_Write(1);
                break;
            case 7:
                //sprintf(direc,"Atras");
                //M1
                EA1_Write(0);
                EB1_Write(1);
                //M2
                EA2_Write(0);
                EB2_Write(1);
                //M3
                EA3_Write(0);
                EB3_Write(1);
                //M4
                EA4_Write(0);
                EB4_Write(1);
                break;
            case 8:
                //sprintf(direc,"SurDerecha");
                //M1
                EA1_Write(0);
                EB1_Write(0);
                //M2
                EA2_Write(0);
                EB2_Write(1);
                //M3
                EA3_Write(0);
                EB3_Write(1);
                //M4
                EA4_Write(0);
                EB4_Write(0);
                break;
            case 9:
                //sprintf(direc,"Rot.Izq");
                //M1
                EA1_Write(0);
                EB1_Write(1);
                //M2
                EA2_Write(1);
                EB2_Write(0);
                //M3
                EA3_Write(0);
                EB3_Write(1);
                //M4
                EA4_Write(1);
                EB4_Write(0);
                break;
            case 10:
                //sprintf(direc,"Rot.Derch");
                //M1
                EA1_Write(1);
                EB1_Write(0);
                //M2
                EA2_Write(0);
                EB2_Write(1);
                //M3
                EA3_Write(1);
                EB3_Write(0);
                //M4
                EA4_Write(0);
                EB4_Write(1);
                break;
            default:
                //sprintf(direc,"DETENIDO");
                //M1
                EA1_Write(0);
                EB1_Write(0);
                //M2
                EA2_Write(0);
                EB2_Write(0);
                //M3
                EA3_Write(0);
                EB3_Write(0);
                //M4
                EA4_Write(0);
                EB4_Write(0);
                break;
            
        }
            }
            partes = strtok(NULL, split);
        }
        
        for(k = n;k>=0;k--){
            strings[k] =' ';
        }
        n=0;
        control=0;
        //perroguardian = 1;
    }
    
    else if(dato == '%'){
        
        // se descompone el string en partes
        partes = strtok(strings, split);
        
        //se procede a usar cada parte para fines distintos
        while(partes != NULL){
            control++;
            if(control == 1){
                cod1 = atoi(partes); // se almacena la "velocidad" en 
            }
            else if(control == 2){
                cod2 = atoi(partes);
                    //ejecutar comandos de direccion    
            }
            partes = strtok(NULL, split);
        }
        
        for(k = n;k>=0;k--){
            strings[k] =' ';
        }
        n=0;
        control=0;
    }
    
    UART_ClearRxBuffer();
    UART_ReadControlRegister();
    ISR_X_ClearPending();
}

void init_hardware(void){
    ISR_X_StartEx(UART_handler);
    ISR_X_ClearPending();
    
    UART_Start();
    UART_Enable();
    
    PWM_Start();
    PWM_Enable();
    
    PWM1_Start();
    PWM1_Enable();
    PWM2_Start();
    PWM2_Enable();
}

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    init_hardware();
    
    for(;;)
    {
        /*
        si la conexion con el respectivo nodo 
        no está establecida, se espera hasta 
        que se establesca y se de orden de 
        ejecutar acciones en el PSoC
        */
        if(cod1 == 0 && cod2 == 0){
            /*
            esperando...
            */
            PWM_WriteCompare(0);
            
            PWM1_WriteCompare1(0);
            PWM1_WriteCompare2(0);
            PWM2_WriteCompare1(0);
            PWM2_WriteCompare2(0);
            
        }
        else if(cod1 == 0 && cod2 == 1){
            //Identificando...
            sprintf(soy,"MOTORES"); //change this part to SENSORES for sensor's PSoC
            UART_PutString(soy);
            PWM_WriteCompare(255);
            
            PWM1_WriteCompare1(0);
            PWM1_WriteCompare2(0);
            PWM2_WriteCompare1(0);
            PWM2_WriteCompare2(0);
            
            cod2 = 0;
        }
        else if(cod1 == 1 && cod2 == 1){
            PWM_WriteCompare(126); // comprobacion visual 
            //conectado a ROS...
            PWM1_WriteCompare1(pwm);
            PWM1_WriteCompare2(pwm);
            PWM2_WriteCompare1(pwm);
            PWM2_WriteCompare2(pwm);
            
        }
    }
}