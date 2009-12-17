#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-msg=C0103

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

from __future__ import absolute_import

from franz import miniclient
from ..exceptions import IllegalArgumentException, ServerException
from ..model import URI, ValueFactory
from .repositoryconnection import RepositoryConnection

import urllib

# * A Sesame repository that contains RDF data that can be queried and updated.
# * Access to the repository can be acquired by opening a connection to it.
# * This connection can then be used to query and/or update the contents of the
# * repository. Depending on the implementation of the repository, it may or may
# * not support multiple concurrent connections.
# * <p>
# * Please note that a repository needs to be initialized before it can be used
# * and that it should be shut down before it is discarded/garbage collected.
# * Forgetting the latter can result in loss of data (depending on the Repository
# * implementation)!
class Repository:
    RENEW = 'RENEW'
    ACCESS = 'ACCESS'
    OPEN = 'OPEN'
    CREATE = 'CREATE'
    REPLACE = 'REPLACE'

    def __init__(self, catalog, database_name, repository):
        self.mini_repository = repository
        self.database_name = database_name
        ## system state fields:
        self.value_factory = None
        self.mapped_predicates = {}
        self.mapped_datatypes = {}
         
    def getDatabaseName(self):
        """
        Return the name of the database (remote triple store) that this repository is
        interfacing with.
        """ 
        return self.database_name
        
    def initialize(self):
        """
        Initializes this repository. A repository needs to be initialized before
        it can be used.  Return 'self' (so that we can chain this call if we like).
        """
        return self

    def listFreeTextPredicates(self):
        return self.mini_repository.listFreeTextPredicates()

    def registerFreeTextPredicate(self, uri=None, namespace=None, localname=None):
        """
        Register a predicate 'uri' (or 'namespace'+'localname'), telling the RDF store to index
        text keywords belonging to strings in object position in the corresponding
        triples/statements.  This is needed to make the  fti:match  operator
        work properly.
        """
        uri = str(uri) or (namespace + localname)
        if not uri.startswith('<'):
            uri = '<' + uri + '>'
        self.mini_repository.registerFreeTextPredicate(uri)
        
    def _translate_inlined_type(self, the_type):
        if the_type == 'int': return '<http://www.w3.org/2001/XMLSchema#int>'
        if the_type == 'datetime': return "<http://www.w3.org/2001/XMLSchema#dateTime>"
        if the_type == 'date': return '<http://www.w3.org/2001/XMLSchema#date>'
        if the_type == "float": return "<http://www.w3.org/2001/XMLSchema#double>"
        raise IllegalArgumentException("Unknown inlined type '%s'\n.  Legal types are " +
                "'int', 'float', and 'datetime'" % the_type)
        
    def registerDatatypeMapping(self, predicate=None, datatype=None, nativeType=None):
        """
        Register an inlined datatype.  If 'predicate', then object arguments to triples
        with that predicate will use an inlined encoding of type 'nativeType' in their 
        internal representation.
        If 'datatype', then typed literal objects with a datatype matching 'datatype' will
        use an inlined encoding of type 'nativeType'.
        """
        predicate = predicate.getURI() if isinstance(predicate, URI) else predicate
        datatype = datatype.getURI() if isinstance(datatype, URI) else datatype
        if predicate:
            if not nativeType:
                raise IllegalArgumentException("Missing 'nativeType' parameter in call to 'registerDatatypeMapping'")
            xsdType = self._translate_inlined_type(nativeType)
            self.mapped_predicates[predicate] = xsdType
            self.mini_repository.addMappedPredicate("<%s>" % predicate, xsdType)            
        elif datatype: 
            xsdType = self._translate_inlined_type(nativeType or datatype)
            self.mapped_datatypes[datatype] = xsdType
            self.mini_repository.addMappedType("<%s>" % datatype, xsdType)
        
    def shutDown(self):
        """
        Shuts the store down, releasing any resources that it keeps hold of.
        Once shut down, the store can no longer be used.
        
        TODO: WE COULD PRESUMABLY ADD SOME LOGIC TO MAKE A RESTART POSSIBLE, ALTHOUGH
        THE ACCESS OPTION MIGHT NOT MAKE SENSE THE SECOND TIME AROUND (KILLING THAT IDEA!)
        """
        self.mini_repository = None

    def isWritable(self):
        """
        Checks whether this store is writable, i.e. if the data contained in
        this store can be changed. The writability of the store is
        determined by the writability of the Sail that this store operates
        on.
        """
        # TODO maybe remove this, it's nonsense in 4.0.
        return True;

    def getConnection(self):
        """
        Opens a connection to this store that can be used for querying and
        updating the contents of the store. Created connections need to be
        closed to make sure that any resources they keep hold of are released. The
        best way to do this is to use a try-finally-block 
        """
        return RepositoryConnection(self)

    def getValueFactory(self):
        """
        Return a ValueFactory for this store
        """
        if not self.value_factory:
            self.value_factory = ValueFactory(self)
        return self.value_factory
