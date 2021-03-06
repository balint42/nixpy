# Copyright (c) 2014, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from __future__ import absolute_import

import sys

import nix.util.find as finders
from nix.core import Block
from nix.util.inject import Inject
from nix.util.proxy_list import ProxyList

class SourceProxyList(ProxyList):

    def __init__(self, obj):
        super(SourceProxyList, self).__init__(obj, "_source_count", "_get_source_by_id",
                                              "_get_source_by_pos", "_delete_source_by_id")


class DataArrayProxyList(ProxyList):

    def __init__(self, obj):
        super(DataArrayProxyList, self).__init__(obj, "_data_array_count", "_get_data_array_by_id",
                                                 "_get_data_array_by_pos", "_delete_data_array_by_id")


class MultiTagProxyList(ProxyList):

    def __init__(self, obj):
        super(MultiTagProxyList, self).__init__(obj, "_multi_tag_count", "_get_multi_tag_by_id",
                                               "_get_multi_tag_by_pos", "_delete_multi_tag_by_id")


class TagProxyList(ProxyList):

    def __init__(self, obj):
        super(TagProxyList, self).__init__(obj, "_tag_count", "_get_tag_by_id",
                                                 "_get_tag_by_pos", "_delete_tag_by_id")


class BlockMixin(Block):

    class __metaclass__(Inject, Block.__class__):
        # this injects all members and the doc into nix.core.Block
        pass

    def find_sources(self, filtr=lambda _ : True, limit=sys.maxint):
        """
        Get all sources in this block recursively.

        This method traverses the tree of all sources in the block. The traversal
        is accomplished via breadth first and can be limited in depth. On each node or
        source a filter is applied. If the filter returns true the respective source
        will be added to the result list.
        By default a filter is used that accepts all sources.

        :param filtr: A filter function
        :type filtr:  function
        :param limit: The maximum depth of traversal
        :type limit:  int

        :returns: A list containing the matching sources.
        :rtype: list of Source
        """
        return finders._find_sources(self, filtr, limit)

    @property
    def sources(self):
        """
        A property containing all sources of a block. Sources can be obtained via their index or by their id.
        Sources can be deleted from the list. Adding sources is done using the Blocks create_source method.
        This is a read only attribute.

        :type: ProxyList of Source entities.
        """
        if not hasattr(self, "_sources"):
            setattr(self, "_sources", SourceProxyList(self))
        return self._sources

    @property
    def multi_tags(self):
        """
        A property containing all multi tags of a block. MultiTag entities can be obtained via their index or by their id.
        Tags can be deleted from the list. Adding tags is done using the Blocks create_multi_tag method.
        This is a read only attribute.

        :type: ProxyList of MultiTag entities.
        """
        if not hasattr(self, "_multi_tags"):
            setattr(self, "_multi_tags", MultiTagProxyList(self))
        return self._multi_tags

    @property
    def tags(self):
        """
        A property containing all tags of a block. Tag entities can be obtained via their index or by their id.
        Tags can be deleted from the list. Adding tags is done using the Blocks create_tag method.
        This is a read only attribute.

        :type: ProxyList of Tag entities.
        """
        if not hasattr(self, "_tags"):
            setattr(self, "_tags", TagProxyList(self))
        return self._tags

    @property
    def data_arrays(self):
        """
        A property containing all data arrays of a block. DataArray entities can be obtained via their index or by their id.
        Data arrays can be deleted from the list. Adding a data array is done using the Blocks create_data_array method.
        This is a read only attribute.

        :type: ProxyList of DataArray entities.
        """
        if not hasattr(self, "_data_arrays"):
            setattr(self, "_data_arrays", DataArrayProxyList(self))
        return self._data_arrays

    def __eq__(self, other):
        """
        Two blocks are considered equal when they have the same id
        """
        if hasattr(other, "id"):
            return self.id == other.id
        else:
            return False
