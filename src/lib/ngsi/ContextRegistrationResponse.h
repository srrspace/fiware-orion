#ifndef SRC_LIB_NGSI_CONTEXTREGISTRATIONRESPONSE_H_
#define SRC_LIB_NGSI_CONTEXTREGISTRATIONRESPONSE_H_

/*
*
* Copyright 2013 Telefonica Investigacion y Desarrollo, S.A.U
*
* This file is part of Orion Context Broker.
*
* Orion Context Broker is free software: you can redistribute it and/or
* modify it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* Orion Context Broker is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
* General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public License
* along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.
*
* For those usages not covered by this license please contact with
* iot_support at tid dot es
*
* Author: Ken Zangelin
*/
#include <string>

#include "ngsi/ContextRegistration.h"
#include "ngsi/StatusCode.h"
#include "ngsi/Request.h"



/* ****************************************************************************
*
* ContextRegistrationResponse -
*/
typedef struct ContextRegistrationResponse
{
  ContextRegistration   contextRegistration;        // Mandatory
  StatusCode            errorCode;                  // Optional
  ProviderFormat        providerFormat;             // During forwarding, this field is used to record the 'format' from the registration that provoked
                                                    // this Context Element to be forwarded.

  ContextRegistrationResponse();

  std::string  toJsonV1(bool comma);
  void         release(void);

  std::string  check(ApiVersion          apiVersion,
                     RequestType         requestType,
                     const std::string&  predetectedError,
                     int                 counter);
} ContextRegistrationResponse;

#endif  // SRC_LIB_NGSI_CONTEXTREGISTRATIONRESPONSE_H_
