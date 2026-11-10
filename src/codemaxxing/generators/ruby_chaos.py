"""Ruby chaos code generator.

Synthesizes rich Ruby source files across multiple distinct archetypes:
Metaprogramming wizardry with define_method and method_missing,
ActiveSupport-style Concerns with callbacks, Ruby 3 pattern matching with Fibers,
and unhinged core monkey-patching extensions.
"""

import random
from io import StringIO

from codemaxxing.generators.base import GeneratedFile, SlopGenerator
from codemaxxing import comments, naming


class RubyChaosGenerator(SlopGenerator):
    """Ruby language code generator.

    Emits dynamic Ruby source code spanning metaprogramming hooks,
    modular concerns, modern pattern matching, and core monkey-patches.
    """

    name = "ruby_chaos"
    language = "ruby"
    extension = ".rb"

    def generate(self, sanity: float, file_index: int) -> GeneratedFile:
        """Generate a synthetic Ruby source file (.rb).

        Args:
            sanity: Chaos/corporate weighting between 0.0 and 1.0.
            file_index: File index for unique filename assignment.

        Returns:
            A `GeneratedFile` containing the synthesized Ruby source code.
        """
        buf = StringIO()
        module_name = naming.class_name(sanity)
        class_name = naming.class_name(sanity)

        buf.write(f"# {comments.comment(sanity)}\n")
        buf.write("# frozen_string_literal: true\n\n")

        archetype = random.choice([
            "metaprogramming_dsl",
            "rails_concern",
            "fiber_pattern_matching",
            "monkey_patch_chaos",
        ])

        if archetype == "metaprogramming_dsl":
            self._generate_metaprogramming(buf, sanity, module_name, class_name)
        elif archetype == "rails_concern":
            self._generate_rails_concern(buf, sanity, module_name, class_name)
        elif archetype == "fiber_pattern_matching":
            self._generate_pattern_matching(buf, sanity, module_name, class_name)
        else:
            self._generate_monkey_patch(buf, sanity, module_name, class_name)

        content = buf.getvalue()
        line_count = content.count("\n")
        filename = f"ruby/{class_name.lower()}_{file_index}{self.extension}"
        return GeneratedFile(filename=filename, content=content, line_count=line_count)

    def _generate_metaprogramming(self, buf: StringIO, sanity: float, mod_name: str, class_name: str) -> None:
        """Emit define_method and method_missing metaprogramming."""
        buf.write(f"module {mod_name}\n")
        buf.write(f"  class {class_name}\n")
        buf.write("    def self.enterprise_attr(*names)\n")
        buf.write("      names.each do |name|\n")
        buf.write("        define_method(name) { instance_variable_get(\"@#{name}\") }\n")
        buf.write("        define_method(\"#{name}=\") { |val| instance_variable_set(\"@#{name}\", val) }\n")
        buf.write("      end\n")
        buf.write("    end\n\n")

        mname = naming.method_name(sanity)
        buf.write(f"    enterprise_attr :{mname}_flag, :correlation_token\n\n")

        buf.write("    def method_missing(method_name, *args, &block)\n")
        buf.write(f"      # {comments.comment(sanity)}\n")
        buf.write("      if method_name.to_s.start_with?('synergize_')\n")
        buf.write("        args.first.to_s.upcase\n")
        buf.write("      else\n")
        buf.write("        super\n")
        buf.write("      end\n")
        buf.write("    end\n\n")

        buf.write("    def respond_to_missing?(method_name, include_private = false)\n")
        buf.write("      method_name.to_s.start_with?('synergize_') || super\n")
        buf.write("    end\n")
        buf.write("  end\n")
        buf.write("end\n")

    def _generate_rails_concern(self, buf: StringIO, sanity: float, mod_name: str, class_name: str) -> None:
        """Emit ActiveSupport::Concern style modular architecture."""
        buf.write(f"module {mod_name}\n")
        buf.write(f"  module {class_name}Concern\n")
        buf.write("    def self.included(base)\n")
        buf.write("      base.extend(ClassMethods)\n")
        buf.write("    end\n\n")
        buf.write("    module ClassMethods\n")
        buf.write("      def configure_telemetry(sink)\n")
        buf.write(f"        # {comments.comment(sanity)}\n")
        buf.write("      end\n")
        buf.write("    end\n")
        buf.write("  end\n")
        buf.write("end\n")

    def _generate_pattern_matching(self, buf: StringIO, sanity: float, mod_name: str, class_name: str) -> None:
        """Emit Ruby 3 pattern matching and tap/then cascades."""
        buf.write(f"module {mod_name}\n")
        buf.write(f"  class {class_name}\n")
        mname = naming.method_name(sanity)
        buf.write(f"    def {mname}(event)\n")
        buf.write("      case event\n")
        buf.write("      in { status: :ok, payload: String => str }\n")
        buf.write("        str.reverse.tap { |s| s.freeze }\n")
        buf.write("      in { status: :error, code: Integer => code }\n")
        buf.write("        \"HALT_#{code}\"\n")
        buf.write("      else\n")
        buf.write("        :unhandled\n")
        buf.write("      end\n")
        buf.write("    end\n")
        buf.write("  end\n")
        buf.write("end\n")

    def _generate_monkey_patch(self, buf: StringIO, sanity: float, mod_name: str, class_name: str) -> None:
        """Emit core monkey patching extensions."""
        buf.write("class ::String\n")
        mname = naming.method_name(sanity)
        buf.write(f"  def {mname}_enterprise\n")
        buf.write(f"    # {comments.comment(sanity)}\n")
        buf.write("    \"[ENTERPRISE] #{self}\"\n")
        buf.write("  end\n")
        buf.write("end\n")
