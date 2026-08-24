#pragma once

/*
 * Keep the original AT firmware indexes stable so persisted settings remain
 * compatible when switching between the AT and OTA examples.
 */
enum
{
    STORAGE_NAME = 1,
    STORAGE_BAUD,
    STORAGE_ATE,
    STORAGE_MODE,
    STORAGE_ADVDATA,
    STORAGE_LSLEEP,
    STORAGE_ADVINTV,
    STORAGE_RFPWR,
    STORAGE_IUUID,
    STORAGE_IMAJOR,
    STORAGE_IMONOR,
    STORAGE_AUTHPWD,
    STORAGE_MTU,
    STORAGE_SPPUUID,
    STORAGE_RXUUID,
    STORAGE_TXUUID,
    STORAGE_CONRANG,
    STORAGE_IBCN_ID,
    STORAGE_IBCN_PWER,
};
