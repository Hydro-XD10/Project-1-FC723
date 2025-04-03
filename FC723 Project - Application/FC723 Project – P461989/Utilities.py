import uuid  # import the uuid module to generate unique identifiers

class Utilities_:
    def __init__(self):
        self.used_references = set()  # store all used references to avoid duplicates

    def generate_reference(self):
        """generate a simple, unique 8-character booking reference"""
        while True:
            ref = uuid.uuid4().hex[:8].upper()  # generate 8 uppercase characters from a uuid
            if ref not in self.used_references:  # check if reference is unique
                self.used_references.add(ref)  # mark the reference as used
                return ref  # return the unique reference