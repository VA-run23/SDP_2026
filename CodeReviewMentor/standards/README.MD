# Effective Java: Core Principles

## Object Creation & Destruction
- **Static Factories**: Use static factory methods instead of constructors for better naming
- **Builders**: Use the Builder pattern when faced with many optional parameters
- **Unnecessary Objects**: Avoid creating unnecessary objects; reuse immutable instances

## Class Design
- **Accessibility**: Minimize the accessibility of classes and members
- **Accessors**: In public classes, use accessor methods (getters/setters), not public fields
- **Inheritance**: Favor composition over inheritance to avoid breaking encapsulation
- **Mutability**: Minimize mutability; make classes immutable unless logic requires otherwise

## Methods & Logic
- **Return Values**: Return empty arrays or collections instead of `null`
- **Loops**: Prefer for-each loops over traditional for loops for readability
- **Exceptions**: Use exceptions only for exceptional conditions, not for flow control