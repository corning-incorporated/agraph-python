#!/usr/bin/env python
# -*- coding: utf-8 -*-

##***** BEGIN LICENSE BLOCK *****
##Version: MPL 1.1
##
##The contents of this file are subject to the Mozilla Public License Version
##1.1 (the "License") you may not use this file except in compliance with
##the License. You may obtain a copy of the License at
##http:##www.mozilla.org/MPL/
##
##Software distributed under the License is distributed on an "AS IS" basis,
##WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
##for the specific language governing rights and limitations under the
##License.
##
##The Original Code is the AllegroGraph Java Client interface.
##
##The Original Code was written by Franz Inc.
##Copyright (C) 2006 Franz Inc.  All Rights Reserved.
##
##***** END LICENSE BLOCK *****


from franz.openrdf.model.value import URI

NS = "http://www.w3.org/2001/XMLSchema#"

class XMLSchema:
    NAMESPACE = NS
    DURATION = URI(namespace=NS, localname="duration")
    DATETIME = URI(namespace=NS, localname="dateTime")
    TIME = URI(namespace=NS, localname="time")
    DATE = URI(namespace=NS, localname="date")
    GYEARMONTH = URI(namespace=NS, localname="gYearMonth")
    GYEAR = URI(namespace=NS, localname="gYear")
    GMONTHDAY = URI(namespace=NS, localname="gMonthDay")
    GDAY = URI(namespace=NS, localname="gDay")
    GMONTH = URI(namespace=NS, localname="gMonth")
    STRING = URI(namespace=NS, localname="string")
    BOOLEAN = URI(namespace=NS, localname="boolean")
    BASE64BINARY = URI(namespace=NS, localname="base64Binary")
    HEXBINARY = URI(namespace=NS, localname="hexBinary")
    FLOAT = URI(namespace=NS, localname="float")
    DECIMAL = URI(namespace=NS, localname="decimal")
    DOUBLE = URI(namespace=NS, localname="double")
    ANYURI = URI(namespace=NS, localname="anyURI")
    QNAME = URI(namespace=NS, localname="QName")
    NOTATION = URI(namespace=NS, localname="NOTATION")
    NORMALIZEDSTRING = URI(namespace=NS, localname="normalizedString")
    TOKEN = URI(namespace=NS, localname="token")
    LANGUAGE = URI(namespace=NS, localname="language")
    NMTOKEN = URI(namespace=NS, localname="NMTOKEN")
    NMTOKENS = URI(namespace=NS, localname="NMTOKENS")
    NAME = URI(namespace=NS, localname="Name")
    NCNAME = URI(namespace=NS, localname="NCName")
    ID = URI(namespace=NS, localname="ID")
    IDREF = URI(namespace=NS, localname="IDREF")
    IDREFS = URI(namespace=NS, localname="IDREFS")
    ENTITY = URI(namespace=NS, localname="ENTITY")
    ENTITIES = URI(namespace=NS, localname="ENTITIES")
    INTEGER = URI(namespace=NS, localname="integer")
    LONG = URI(namespace=NS, localname="long")
    INT = URI(namespace=NS, localname="int")
    SHORT = URI(namespace=NS, localname="short")
    NUMBER = URI(namespace=NS, localname="number")        
    BYTE = URI(namespace=NS, localname="byte")
    NON_POSITIVE_INTEGER = URI(namespace=NS, localname="nonPositiveInteger")
    NEGATIVE_INTEGER = URI(namespace=NS, localname="negativeInteger")
    NON_NEGATIVE_INTEGER = URI(namespace=NS, localname="nonNegativeInteger")
    POSITIVE_INTEGER = URI(namespace=NS, localname="positiveInteger")
    UNSIGNED_LONG = URI(namespace=NS, localname="unsignedLong")
    UNSIGNED_INT = URI(namespace=NS, localname="unsignedInt")
    UNSIGNED_SHORT = URI(namespace=NS, localname="unsignedShort")
    UNSIGNED_BYTE = URI(namespace=NS, localname="unsignedByte")        

    ## map of uri strings to URI objects:
    uristr2obj = {}
    
for name, uri in XMLSchema.__dict__.iteritems():
    if name.upper() == name:
        XMLSchema.uristr2obj[str(uri)] = uri

del XMLSchema.uristr2obj[NS]
