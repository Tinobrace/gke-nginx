# -*- coding: utf-8 -*- #
# Copyright 2024 Google LLC. All Rights Reserved.
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
"""Implementation of command for deleting folders."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.storage import errors_util
from googlecloudsdk.command_lib.storage import flags
from googlecloudsdk.command_lib.storage import folder_util
from googlecloudsdk.command_lib.storage import name_expansion
from googlecloudsdk.command_lib.storage import rm_command_util
from googlecloudsdk.command_lib.storage import storage_url
from googlecloudsdk.command_lib.storage.tasks import task_graph_executor


@base.DefaultUniverseOnly
class Delete(base.Command):
  """Delete folders."""

  detailed_help = {
      'DESCRIPTION': """Delete folders.""",
      'EXAMPLES': """
      The following command deletes a folder named `folder`
      in a hierarchical namesapce bucket
      called `my-bucket`:

        $ {command} gs://my-bucket/folder/
      """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'urls',
        type=str,
        nargs='+',
        help='The URLs of the folders to delete.',
    )
    flags.add_additional_headers_flag(parser)

  def Run(self, args):
    for url_string in args.urls:
      url = storage_url.storage_url_from_string(url_string)
      errors_util.raise_error_if_not_gcs_folder_type(
          args.command_path, url, 'folder'
      )

    folder_expansion_iterator = name_expansion.NameExpansionIterator(
        args.urls,
        folder_setting=folder_util.FolderSetting.LIST_WITHOUT_OBJECTS,
        raise_error_for_unmatched_urls=True,
    )
    self.exit_code = rm_command_util.remove_folders(
        folder_expansion_iterator,
        task_status_queue=task_graph_executor.multiprocessing_context.Queue(),
        raise_error_for_unmatched_urls=True,
    )
