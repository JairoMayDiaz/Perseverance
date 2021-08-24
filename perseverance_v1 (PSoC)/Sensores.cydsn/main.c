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
char strings[20];
char dato;
char imp[99];
const char split[]=",";
char *partes;
char to_ros[20]="";
int control;
int n=0;
//////////////////////////////////////////////////////////

/////////////////////variables para comunicacion//////////
volatile int cod1 = 0;
volatile int cod2 = 0;
char soy[20]="";
//////////////////////////////////////////////////////////

/////////////////////variables de Distancia///////////////
volatile float distance;
int timer_counts = 0;
/////////////////////variables de RPM///////////////
volatile int counts_1 = 0;
volatile int counts_2 = 0;
volatile int counts_3 = 0;
volatile int counts_4 = 0;

CY_ISR(UART_handler){
    
    // se toma cada caracter por interrupcion
    dato = UART_GetChar();
    // y se almacena en un array
    strings[n]=dato;
    //si el caracter no es "#" se agrega un espacio
    if(dato != '%'){n++;}
    /*
    --La funcion siguiente desenpeña el mismo trabajo que el anterior
    --Este se usa para codigos de configuracion
    */
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
        
        for(n=20;n>=0;n--){
            strings[n] =' ';
        }
        n=0;
        control=0;
    }
    
    UART_ClearRxBuffer();
    UART_ReadControlRegister();
    ISR_X_ClearPending();
}

CY_ISR(ultrasonic_handler){
    timer_counts = 65535 - Timer_ReadCapture();
    distance = timer_counts/58;
    Timer_ReadStatusRegister();
}

CY_ISR(Decoder1_handler){
    counts_2 = Counter_1_ReadCapture();
    counts_4 = Counter_2_ReadCapture();
    counts_3 = Counter_3_ReadCapture();
    counts_1 = Counter_4_ReadCapture();
    
    Counter_1_ReadStatusRegister();
    Counter_2_ReadStatusRegister();
    Counter_3_ReadStatusRegister();
    Counter_4_ReadStatusRegister();
    
    Counter_1_Init();
    Counter_2_Init();
    Counter_3_Init();
    Counter_4_Init();
    
}
void init_hardware(void){
    
    ISR_X_StartEx(UART_handler);
    ISR_X_ClearPending();
    
    isr_timer_StartEx(ultrasonic_handler);
    isr_timer_ClearPending();
    
    isr_mots_StartEx(Decoder1_handler);
    isr_mots_ClearPending();
    
    UART_Start();
    UART_Enable();
    
    Timer_Start();
    
    PWM_Start();
    PWM_Enable();
    
    PWM_mots_Start();
    PWM_mots_Enable();
    
    Counter_1_Start();
    Counter_1_Enable();
    
    Counter_2_Start();
    Counter_2_Enable();
    
    Counter_3_Start();
    Counter_3_Enable();
    
    Counter_4_Start();
    Counter_4_Enable();
    
}

void Ultra_trigger(void){
    while(Echo_Read()==0)//condición de espera para implementar la secuencia de inicio
    { 
        Trigger_out_Write(1);//activar en 1 lógico la salida al pin trigg y el reinicio del timer
        CyDelay(10u);        //Espera de 10uS para la activación de envío de ráfagas
        Trigger_out_Write(0);//Desactivar el pin trigg generando así el pulso de entrada
        CyDelay(1);
        if(distance <= 11.0 && distance >= 0){
            break;
        }
    }
}

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */

    init_hardware();
    
    //the line below is for naming the PSoC duty.
    //sprintf(soy,"device");
    
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
            
        }
        else if(cod1 == 0 && cod2 == 1){
            //Identificando...
            sprintf(soy,"SENSORES"); //change this part to SENSORES for sensor's PSoC
            UART_PutString(soy);
            PWM_WriteCompare(255);
            cod2 = 0;
        }
        else if(cod1 == 1 && cod2 == 1){
            PWM_WriteCompare(126); // comprobacion visual 
            //conectado a ROS...
            Ultra_trigger();
            sprintf(to_ros,"%d,%d,%d,%d,%.2f\r\n",counts_1,counts_2,counts_3,counts_4,distance);
            UART_PutString(to_ros);
        }
    }
}