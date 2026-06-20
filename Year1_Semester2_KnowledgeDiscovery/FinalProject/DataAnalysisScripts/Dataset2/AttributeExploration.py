class AttributeExplorer:
    """
    Executes interactive Attribute Exploration using the Next-Closure algorithm.
    Manages a formal context and queries standard input to validate implications.
    """

    def __init__(self, initial_context: dict, attributes: list):
        """
        Initializes the explorer with a starting dataset and a defined list of attributes.
        initial_context: Dictionary mapping object identifiers to sets of attributes.
        attributes: Ordered list of all possible attributes in the domain.
        """
        self.context = initial_context
        self.attributes = attributes
        self.stem_base = []

    def _compute_attribute_closure(self, attribute_set: frozenset) -> frozenset:
        """
        Computes the attribute closure in the current formal context.
        Identifies all objects containing the given attribute set, then returns
        the intersection of all attributes possessed by those specific objects.
        """
        if not attribute_set:
            objects = set(self.context.keys())
        else:
            objects = {obj_id for obj_id, attrs in self.context.items() if attribute_set.issubset(attrs)}

        if not objects:
            all_attrs = set()
            for attrs in self.context.values():
                all_attrs.update(attrs)
            return frozenset(all_attrs)

        obj_list = list(objects)
        result = set(self.context[obj_list[0]])
        for obj_id in obj_list[1:]:
            result.intersection_update(self.context[obj_id])

        return frozenset(result)

    def _compute_implicational_closure(self, attribute_set: frozenset) -> frozenset:
        """
        Computes the implicational closure under the currently accepted stem base.
        Applies verified rules to expand the attribute set until no new attributes are added.
        """
        current_set = set(attribute_set)
        changed = True

        while changed:
            changed = False
            for premise, conclusion in self.stem_base:
                if premise.issubset(current_set):
                    new_set = current_set | conclusion
                    if len(new_set) > len(current_set):
                        current_set = new_set
                        changed = True

        return frozenset(current_set)

    def explore(self) -> list:
        """
        Executes the interactive Next-Closure exploration loop.
        Outputs proposed rules to the console and requires standard input for validation.
        Returns the final list of verified implications.
        """
        current_closed_set = self._compute_attribute_closure(frozenset())
        total_attributes = len(self.attributes)

        while current_closed_set != frozenset(self.attributes):
            found_next = False

            for i in range(total_attributes - 1, -1, -1):
                current_attribute = self.attributes[i]

                if current_attribute not in current_closed_set:
                    prefix = frozenset(self.attributes[:i])
                    candidate_set = (current_closed_set & prefix) | {current_attribute}
                    implicational_set = self._compute_implicational_closure(candidate_set)

                    if implicational_set & prefix == current_closed_set & prefix:
                        attribute_closure = self._compute_attribute_closure(implicational_set)

                        if implicational_set != attribute_closure:
                            premise = implicational_set
                            conclusion = attribute_closure - premise

                            print(f"\n--- PROPOSED RULE ---")
                            print(f"IF an object has: {list(premise)}")
                            print(f"THEN it MUST also have: {list(conclusion)}")

                            user_input = input("Accept rule? (y/n): ").strip().lower()

                            if user_input == 'y':
                                self.stem_base.append((premise, conclusion))
                                print("Rule added to Stem Base.")
                            else:
                                print("\nRule rejected. A counterexample is required.")
                                new_obj_name = input("Enter an ID for the new counterexample object: ").strip()
                                new_attrs_str = input("Enter comma-separated attributes for this object: ").strip()

                                new_attrs = set([attr.strip() for attr in new_attrs_str.split(",") if attr.strip()])
                                self.context[new_obj_name] = new_attrs

                                print(f"Counterexample '{new_obj_name}' added to the formal context.")

                                # Recompute the current closed set as the context has changed
                                current_closed_set = self._compute_attribute_closure(current_closed_set)
                                break

                        else:
                            current_closed_set = implicational_set
                            found_next = True
                            break

            if not found_next and current_closed_set == frozenset(self.attributes):
                break
            elif not found_next:
                current_closed_set = frozenset(self.attributes)

        print("\n--- EXPLORATION COMPLETE ---")
        return self.stem_base


# Script execution block
if __name__ == "__main__":
    # Define the domain attributes based on the continuous casting dataset
    attributes = ["Short_Sequence", "High_Speed", "High_Resistance", "Critical_RUL"]

    # Initialize a small starting context (historical data examples)
    initial_context = {
        "Cast_1": {"Short_Sequence", "High_Resistance", "Critical_RUL"},
        "Cast_2": {"High_Speed"}
    }

    explorer = AttributeExplorer(initial_context, attributes)
    final_rules = explorer.explore()

    print("\nFinal Verified Rules (Stem Base):")
    for premise, conclusion in final_rules:
        print(f"{list(premise)} -> {list(conclusion)}")