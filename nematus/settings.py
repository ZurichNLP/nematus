#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration containers.
"""

import uuid

class DecoderSettings(object):

    def __init__(self, parsed_console_arguments=None):
        """
        Decoder settings are initialised with default values, unless parsed
        console arguments as returned by a `ConsoleInterface`'s `parse_args()`
        method are provided.
        """
        self.models = []
        self.num_processes = 1
        self.device_list = []
        self.verbose = False
        self.num_attentions = 1
        self.num_encoders = 1
        self.multisource = None
        if parsed_console_arguments:
            self.update_from(parsed_console_arguments)

    def update_from(self, parsed_console_arguments):
        """
        Updates decoder settings based on @param parsed_console_arguments,
        as returned by a `ConsoleInterface`'s `parse_args()` method.
        """
        args = parsed_console_arguments
        self.models = args.models
        self.num_processes = args.p
        self.device_list = args.device_list
        self.verbose = args.v

        # multisource
        if not hasattr(args, 'aux_input'):
            self.multisource = False
            self.num_inputs = 1
        elif len(args.aux_input) > 0:
            self.multisource = True
            self.num_inputs = len(args.aux_input) + 1
        else:
            self.multisource = False
            self.num_inputs = 1


class TranslationSettings(object):

    ALIGNMENT_TEXT = 1
    ALIGNMENT_JSON = 2

    def __init__(self, parsed_console_arguments=None):
        """
        Translation settings are initialised with default values, unless parsed
        console arguments as returned by a `ConsoleInterface`'s `parse_args()`
        method are provided.
        """
        self.request_id = uuid.uuid4()
        self.beam_width = 5
        self.normalization_alpha = 0.0
        self.char_level = False
        self.n_best = 1
        self.suppress_unk = False
        self.get_word_probs = False
        self.get_alignment = False
        self.alignment_type = None
        self.alignment_filename = None
        self.aux_alignment_filenames = []
        self.get_search_graph = False
        self.search_graph_filename = None
        self.multisource = False
        self.predicted_trg = False
        if parsed_console_arguments:
            self.update_from(parsed_console_arguments)

    def update_from(self, parsed_console_arguments):
        """
        Updates translation settings based on @param parsed_console_arguments,
        as returned by a `ConsoleInterface`'s `parse_args()` method.
        """
        args = parsed_console_arguments
        self.beam_width = args.k
        self.normalization_alpha = args.n
        self.char_level = args.c
        self.n_best = args.n_best
        self.suppress_unk = args.suppress_unk
        self.get_word_probs = args.print_word_probabilities

        if args.output_alignment:
            self.get_alignment = True
            self.alignment_filename = args.output_alignment

            # alignments for multiple inputs
            for i in range(len(args.aux_input)):
                self.aux_alignment_filenames.append(file(args.output_alignment.name + '_aux'+str(i+1), 'w'))
            if args.json_alignment:
                self.alignment_type = self.ALIGNMENT_JSON
            else:
                self.alignment_type = self.ALIGNMENT_TEXT
        else:
            self.get_alignment = False
        if args.search_graph:
            self.get_search_graph = True
            self.search_graph_filename = args.search_graph
        else:
            self.get_search_graph = False
            self.search_graph_filename = None

        if args.aux_input is not None:
            self.multisource = True
        else:
            self.multisource = False

        self.predicted_trg = args.predicted_trg


class ServerSettings(object):

    def __init__(self, parsed_console_arguments=None):
        """
        Server settings are initialised with default values, unless parsed
        console arguments as returned by a `ConsoleInterface`'s `parse_args()`
        method are provided.
        """
        self.style = "Nematus" #TODO: use constant
        self.host = "localhost"
        self.port = 8080
        if parsed_console_arguments:
            self.update_from(parsed_console_arguments)

    def update_from(self, parsed_console_arguments):
        """
        Updates decoder settings based on @param parsed_console_arguments,
        as returned by a `ConsoleInterface`'s `parse_args()` method.
        """
        args = parsed_console_arguments
        self.style = args.style
        self.host = args.host
        self.port = args.port
