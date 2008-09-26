#!/usr/bin/env python
# -*- coding: utf-8 -*-

##***** BEGIN LICENSE BLOCK *****
##Version: MPL 1.1
##
##The contents of this file are subject to the Mozilla Public License Version
##1.1 (the "License"); you may not use this file except in compliance with
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


from franz.openrdf.exceptions import *
from franz.openrdf.repository.jdbcresultset import JDBCResultSet
from franz.openrdf.query.queryresult import TupleQueryResult

class QueryLanguage:
    registered_languages = []
    SPARQL = None
    PROLOG = None
    def __init__(self, name):
        self.name = name
        QueryLanguage.registered_languages.append(self)
        
    def __str__(self): return self.name
    
    def getName(self): return self.name

    @staticmethod
    def values(): return QueryLanguage.registered_languages[:]
    
    @staticmethod
    def valueOf(name): 
        for ql in QueryLanguage.registered_languages:
            if ql.name.lower() == name.lower():
                return ql
        return None
    
QueryLanguage.SPARQL = QueryLanguage('SPARQL')
QueryLanguage.PROLOG = QueryLanguage('PROLOG')

#############################################################################
##
#############################################################################

class Query(object):
    """
    A query on a {@link Repository} that can be formulated in one of the
    supported query languages (for example SeRQL or SPARQL). It allows one to
    predefine bindings in the query to be able to reuse the same query with
    different bindings.
    """
    def __init__(self, queryLanguage, queryString, baseURI=None):
        self.queryLanguage = queryLanguage
        self.queryString = queryString
        self.baseURI = baseURI
        self.dataset = None
        self.includeInferred = False

    def setBinding(self, name, value):
        """
        Binds the specified variable to the supplied value. Any value that was
        previously bound to the specified value will be overwritten.
        """
        self.bindings.addBinding(name, value)

    def removeBinding(self, name):
        """ 
        Removes a previously set binding on the supplied variable. Calling this
        method with an unbound variable name has no effect.
        """ 
        self.bindings.removeBinding(name)

    def getBindings(self):
        """
        Retrieves the bindings that have been set on this query. 
        """ 
        return self.bindings

    def setDataset(self, dataset):
        """
        Specifies the dataset against which to evaluate a query, overriding any
        dataset that is specified in the query itself. 
        """ 
        self.dataset = dataset
     
    def getDataset(self):
        """
        Gets the dataset that has been set using {@link #setDataset(Dataset)}, if  any. 
        """ 
        return self.dataset
     
    def setIncludeInferred(self, includeInferred):
        """
        Determine whether evaluation results of this query should include inferred
        statements (if any inferred statements are present in the repository). The
        default setting is 'true'. 
        """ 
        self.includeInferred = includeInferred

    def getIncludeInferred(self):
        """
        Returns whether or not this query will return inferred statements (if any
        are present in the repository). 
        """ 
        return self.includeInferred
    
    @staticmethod
    def _check_language(self, queryLanguage):
        if not queryLanguage in [QueryLanguage.SPARQL, QueryLanguage.PROLOG]:
            raise IllegalOptionException("Can't evaluate the query language '%s'.  Options are: SPARQL and PROLOG."
                                         % queryLanguage)
    

#############################################################################
##
#############################################################################

class TupleQuery(Query):
    def __init__(self, queryLanguage, queryString, baseURI=None):
        Query._check_language(queryLanguage)
        super(TupleQuery, self).__init__(queryLanguage, queryString, baseURI=baseURI)
        self.connection = None
        
    def setConnection(self, connection):
        """
        Internal call to embed the connection into the query.
        """
        self.connection = connection
    
    def evaluate(self, jdbc=False):
        """
        Execute the embedded query against the RDF store.  Return
        an iterator that produces for each step a tuple of values
        (resources and literals) corresponding to the variables
        or expressions in a 'select' clause (or its equivalent).
        If 'jdbc', returns a JDBC-style iterator that miminizes the
        overhead of creating response objects.        
        TODO: DOESN'T TAKE DATASETS INTO ACCOUNT.  THAT NEEDS TO BE COMMUNICATED
        TO THE SERVER SOMEHOW.      
        """
        ## before executing, see if there is a dataset that needs to be incorporated into the query
        if self.dataset:
            raise UnimplementedMethodException("Query datasets not yet implemented")
        mini = self.connection.mini_repository
        if self.queryLanguage == QueryLanguage.SPARQL:
            ## THIS IS BOGUS; WE GET BACK COLUMN NAMES AND TUPLES:
            response = mini.evalSparqlQuery(self.queryString)
        elif self.queryLanguage == QueryLanguage.PROLOG:
            response = mini.evalPrologQuery(self.queryString)
        if jdbc:
                raise UnimplementedMethodException("'jdbc' option not yet implemented for 'evaluate'")
        else:
            return TupleQueryResult(response['names'], response['values'])

class GraphQuery(Query):
    
    def evaluate(self):
        """
        Execute the embedded query against the RDF store.  Return
        an iterator that produces for each step a Statement.
        """
        raise UnimplementedMethodException("evaluate")

class BooleanQuery(Query):
    
    def evaluate(self):
        """
        Execute the embedded query against the RDF store.  Return
        true or false
        """
        raise UnimplementedMethodException("evaluate")


