# -*- coding: utf-8 -*- #
# Copyright 2017 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for listing available configurations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import commands
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import platforms
from googlecloudsdk.command_lib.run import pretty_print
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core import log


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.GA)
class List(commands.List):
  """List available Configurations.

  Every Configuration is paired with a Service of the same name.
  """

  detailed_help = {
      'DESCRIPTION': """\
          {description}
          """,
      'EXAMPLES': """\
          To list available services:

              $ {command}
          """,
  }

  @classmethod
  def CommonArgs(cls, parser):
    # Flags specific to connecting to a cluster
    namespace_presentation = presentation_specs.ResourcePresentationSpec(
        '--namespace',
        resource_args.GetNamespaceResourceSpec(),
        'Namespace to list configurations in.',
        required=True,
        prefixes=False,
        hidden=True)
    concept_parsers.ConceptParser(
        [namespace_presentation]).AddToParser(parser)

    parser.display_info.AddUriFunc(cls._GetResourceUri)

  @classmethod
  def Args(cls, parser):
    cls.CommonArgs(parser)

  def _SetFormat(self, args, show_region=False, show_namespace=False):
    """Set display format for output.

    Args:
      args: Namespace, the args namespace
      show_region: bool, True to show region of listed services
      show_namespace: bool, True to show namespace of listed services
    """
    columns = [
        pretty_print.READY_COLUMN,
        'firstof(id,metadata.name):label=CONFIGURATION',
    ]
    if show_region:
      columns.append('region:label=REGION')
    if show_namespace:
      columns.append('namespace:label=NAMESPACE')
    columns.extend([
        'status.latestCreatedRevisionName:label="LATEST REVISION"',
        'status.latestReadyRevisionName:label="READY REVISION"',
    ])
    args.GetDisplayInfo().AddFormat(
        'table({columns}):({alias})'.format(
            columns=','.join(columns), alias=commands.SATISFIES_PZS_ALIAS
        )
    )

  def Run(self, args):
    """List available configurations."""
    is_managed = platforms.GetPlatform() == platforms.PLATFORM_MANAGED
    conn_context = connection_context.GetConnectionContext(
        args, flags.Product.RUN, self.ReleaseTrack())
    self._SetFormat(
        args, show_region=is_managed, show_namespace=(not is_managed))
    namespace_ref = args.CONCEPTS.namespace.Parse()
    with serverless_operations.Connect(conn_context) as client:
      self.SetCompleteApiEndpoint(conn_context.endpoint)
      if not is_managed:
        zone_label = ' in zone [{}]'.format(conn_context.cluster_location)
        log.status.Print('For cluster [{cluster}]{zone}:'.format(
            cluster=conn_context.cluster_name,
            zone=zone_label if conn_context.cluster_location else ''))
      return commands.SortByName(client.ListConfigurations(namespace_ref))


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class AlphaList(List):
  """List available Configurations.

  Every Configuration is paired with a Service of the same name.
  """

  @classmethod
  def Args(cls, parser):
    cls.CommonArgs(parser)

AlphaList.__doc__ = List.__doc__
