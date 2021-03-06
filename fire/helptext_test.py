# Copyright (C) 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the helptext module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import textwrap

from fire import helptext
from fire import inspectutils
from fire import test_components as tc
from fire import testutils
from fire import trace


class HelpTest(testutils.BaseTestCase):

  def setUp(self):
    os.environ['ANSI_COLORS_DISABLED'] = '1'

  def testHelpTextNoDefaults(self):
    component = tc.NoDefaults
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, name='NoDefaults'))
    self.assertIn('NAME\n    NoDefaults', help_screen)
    self.assertIn('SYNOPSIS\n    NoDefaults', help_screen)
    self.assertNotIn('DESCRIPTION', help_screen)
    self.assertNotIn('NOTES', help_screen)

  def testHelpTextNoDefaultsObject(self):
    component = tc.NoDefaults()
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, name='NoDefaults'))
    self.assertIn('NAME\n    NoDefaults', help_screen)
    self.assertIn('SYNOPSIS\n    NoDefaults COMMAND', help_screen)
    self.assertNotIn('DESCRIPTION', help_screen)
    self.assertIn('COMMANDS\n    COMMAND is one of the followings:',
                  help_screen)
    self.assertIn('double', help_screen)
    self.assertIn('triple', help_screen)
    self.assertNotIn('NOTES', help_screen)

  def testHelpTextFunction(self):
    component = tc.NoDefaults().double
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, name='double'))
    self.assertIn('NAME\n    double', help_screen)
    self.assertIn('SYNOPSIS\n    double COUNT', help_screen)
    self.assertNotIn('DESCRIPTION', help_screen)
    self.assertIn('POSITIONAL ARGUMENTS\n    COUNT', help_screen)
    self.assertIn(
        'NOTES\n    You could also use flags syntax for POSITIONAL ARGUMENTS',
        help_screen)

  def testHelpTextFunctionWithDefaults(self):
    component = tc.WithDefaults().triple
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, name='triple'))
    self.assertIn('NAME\n    triple', help_screen)
    self.assertIn('SYNOPSIS\n    triple [--count=COUNT]', help_screen)
    self.assertNotIn('DESCRIPTION', help_screen)
    self.assertIn('FLAGS\n    --count', help_screen)
    self.assertNotIn('NOTES', help_screen)

  def testHelpTextFunctionWithBuiltin(self):
    component = 'test'.upper
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, 'upper'))
    self.assertIn('NAME\n    upper', help_screen)
    self.assertIn('SYNOPSIS\n    upper', help_screen)
    # We don't check description content here since the content is python
    # version dependent.
    self.assertIn('DESCRIPTION\n', help_screen)
    self.assertNotIn('NOTES', help_screen)

  def testHelpTextFunctionIntType(self):
    component = int
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component, info=info, trace=trace.FireTrace(component, 'int'))
    self.assertIn('NAME\n    int', help_screen)
    self.assertIn('SYNOPSIS\n    int', help_screen)
    # We don't check description content here since the content is python
    # version dependent.
    self.assertIn('DESCRIPTION\n', help_screen)

  def testHelpTextEmptyList(self):
    component = []
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, 'list'))
    self.assertIn('NAME\n    list', help_screen)
    self.assertIn('SYNOPSIS\n    list COMMAND', help_screen)
    # We don't check description content here since the content could be python
    # version dependent.
    self.assertIn('DESCRIPTION\n', help_screen)
    # We don't check the listed commands either since the list API could
    # potentially change between Python versions.
    self.assertIn('COMMANDS\n    COMMAND is one of the followings:\n',
                  help_screen)

  def testHelpTextShortList(self):
    component = [10]
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, 'list'))
    self.assertIn('NAME\n    list', help_screen)
    self.assertIn('SYNOPSIS\n    list COMMAND', help_screen)
    # We don't check description content here since the content could be python
    # version dependent.
    self.assertIn('DESCRIPTION\n', help_screen)

    # We don't check the listed commands comprehensively since the list API
    # could potentially change between Python versions. Check a few
    # functions(command) that we're confident likely remain available.
    self.assertIn('COMMANDS\n    COMMAND is one of the followings:\n',
                  help_screen)
    self.assertIn('     append\n', help_screen)

  def testHelpTextInt(self):
    component = 7
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component, info=info, trace=trace.FireTrace(component, '7'))
    self.assertIn('NAME\n    7', help_screen)
    self.assertIn('SYNOPSIS\n    7 COMMAND | VALUE', help_screen)
    self.assertIn('DESCRIPTION\n', help_screen)
    self.assertIn('COMMANDS\n    COMMAND is one of the followings:\n',
                  help_screen)
    self.assertIn('VALUES\n    VALUE is one of the followings:\n', help_screen)

  def testHelpTextNoInit(self):
    component = tc.OldStyleEmpty
    info = inspectutils.Info(component)
    help_screen = helptext.HelpText(
        component=component,
        info=info,
        trace=trace.FireTrace(component, 'OldStyleEmpty'))
    self.assertIn('NAME\n    OldStyleEmpty', help_screen)
    self.assertIn('SYNOPSIS\n    OldStyleEmpty', help_screen)

  def testHelpScreen(self):
    component = tc.ClassWithDocstring()
    t = trace.FireTrace(component, name='ClassWithDocstring')
    info = inspectutils.Info(component)
    help_output = helptext.HelpText(component, info, t)
    expected_output = """
NAME
    ClassWithDocstring - Test class for testing help text output.

SYNOPSIS
    ClassWithDocstring COMMAND | VALUE

DESCRIPTION
    This is some detail description of this test class.

COMMANDS
    COMMAND is one of the followings:

     print_msg
       Prints a message.

VALUES
    VALUE is one of the followings:

     message
       The default message to print.
"""
    self.assertEqual(textwrap.dedent(expected_output).strip(),
                     help_output.strip())

  def testHelpScreenForFunctionDocstringWithLineBreak(self):
    component = tc.ClassWithMultilineDocstring.example_generator
    t = trace.FireTrace(component, name='example_generator')
    info = inspectutils.Info(component)
    help_output = helptext.HelpText(component, info, t)
    expected_output = """
    NAME
        example_generator - Generators have a ``Yields`` section instead of a ``Returns`` section.

    SYNOPSIS
        example_generator N

    DESCRIPTION
        Generators have a ``Yields`` section instead of a ``Returns`` section.

    POSITIONAL ARGUMENTS
        N
            The upper limit of the range to generate, from 0 to `n` - 1.

    NOTES
        You could also use flags syntax for POSITIONAL ARGUMENTS
    """
    self.assertEqual(textwrap.dedent(expected_output).strip(),
                     help_output.strip())

  def testHelpScreenForFunctionFunctionWithDefaultArgs(self):
    component = tc.WithDefaults().double
    t = trace.FireTrace(component, name='double')
    info = inspectutils.Info(component)
    help_output = helptext.HelpText(component, info, t)
    expected_output = """
    NAME
        double - Returns the input multiplied by 2.

    SYNOPSIS
        double [--count=COUNT]

    DESCRIPTION
        Returns the input multiplied by 2.

    FLAGS
        --count
          Input number that you want to double.
    """
    self.assertEqual(textwrap.dedent(expected_output).strip(),
                     help_output.strip())


class UsageTest(testutils.BaseTestCase):

  def testUsageOutput(self):
    component = tc.NoDefaults()
    t = trace.FireTrace(component, name='NoDefaults')
    info = inspectutils.Info(component)
    usage_output = helptext.UsageText(component, info, trace=t, verbose=False)
    expected_output = '''
    Usage: NoDefaults <command>
      available commands:    double | triple

    For detailed information on this command and its flags, run:
    NoDefaults --help
    '''

    self.assertEqual(
        usage_output,
        textwrap.dedent(expected_output).lstrip('\n'))

  def testUsageOutputVerbose(self):
    component = tc.NoDefaults()
    t = trace.FireTrace(component, name='NoDefaults')
    info = inspectutils.Info(component)
    usage_output = helptext.UsageText(component, info, trace=t, verbose=True)
    expected_output = '''
    Usage: NoDefaults <command>
      available commands:    double | triple

    For detailed information on this command and its flags, run:
    NoDefaults --help
    '''
    self.assertEqual(
        usage_output,
        textwrap.dedent(expected_output).lstrip('\n'))

  def testUsageOutputMethod(self):
    component = tc.NoDefaults().double
    t = trace.FireTrace(component, name='NoDefaults')
    t.AddAccessedProperty(component, 'double', ['double'], None, None)
    info = inspectutils.Info(component)
    usage_output = helptext.UsageText(component, info, trace=t, verbose=True)
    expected_output = '''
    Usage: NoDefaults double COUNT

    For detailed information on this command, run:
    NoDefaults double --help
    '''
    self.assertEqual(
        usage_output,
        textwrap.dedent(expected_output).lstrip('\n'))

  def testUsageOutputFunctionWithHelp(self):
    component = tc.function_with_help
    t = trace.FireTrace(component, name='function_with_help')
    info = inspectutils.Info(component)
    usage_output = helptext.UsageText(component, info, trace=t, verbose=True)
    expected_output = '''
    Usage: function_with_help <flags>

    Available flags: --help

    For detailed information on this command, run:
    function_with_help -- --help
    '''
    self.assertEqual(
        usage_output,
        textwrap.dedent(expected_output).lstrip('\n'))

  def testUsageOutputFunctionWithDocstring(self):
    component = tc.multiplier_with_docstring
    t = trace.FireTrace(component, name='multiplier_with_docstring')
    info = inspectutils.Info(component)
    usage_output = helptext.UsageText(component, info, trace=t, verbose=True)
    expected_output = '''
    Usage: multiplier_with_docstring NUM <flags>

    Available flags: --rate

    For detailed information on this command, run:
    multiplier_with_docstring --help
    '''
    self.assertEqual(
        usage_output,
        textwrap.dedent(expected_output).lstrip('\n'))

  @testutils.skip('The functionality is not implemented yet')
  def testUsageOutputCallable(self):
    # This is both a group and a command!
    component = tc.CallableWithKeywordArgument
    t = trace.FireTrace(component, name='CallableWithKeywordArgument')
    info = inspectutils.Info(component)
    usage_output = helptext.UsageText(component, info, trace=t, verbose=True)
    # TODO(zuhaohen): We need to handle the case for keyword args as well
    # i.e. __call__ method of CallableWithKeywordArgument
    expected_output = '''
    Usage: CallableWithKeywordArgument <command>

      Available commands:    print_msg

    For detailed information on this command, run:
    CallableWithKeywordArgument -- --help
    '''
    self.assertEqual(
        usage_output,
        textwrap.dedent(expected_output).lstrip('\n'))

  def testUsageOutputConstructorWithParameter(self):
    component = tc.InstanceVars
    t = trace.FireTrace(component, name='InstanceVars')
    info = inspectutils.Info(component)
    usage_output = helptext.UsageText(component, info, trace=t, verbose=True)
    expected_output = '''
    Usage: InstanceVars ARG1 ARG2

    For detailed information on this command, run:
    InstanceVars --help
    '''
    self.assertEqual(
        usage_output,
        textwrap.dedent(expected_output).lstrip('\n'))


if __name__ == '__main__':
  testutils.main()
