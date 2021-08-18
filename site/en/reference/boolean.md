---
id: boolean.md
title: Boolean Expression Rules
---

# Boolean Expression Rules

[EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) grammar rules describes boolean expressions rules. Boolean expression rules are as follows:

```
Expr = LogicalExpr | NIL

LogicalExpr = LogicalExpr BinaryLogicalOp LogicalExpr 
              | UnaryLogicalOp LogicalExpr
              | "(" LogicalExpr ")"
              | SingleExpr;

BinaryLogicalOp = "&&" | "and" | "||" | "or";

UnaryLogicalOp = "not";

SingleExpr = TermExpr | CompareExpr;

TermExpr = IDENTIFIER "in" ConstantArray;

Constant = INTERGER | FLOAT

ConstantExpr = Constant
               | ConstantExpr BinaryArithOp ConstantExpr
               | UnaryArithOp ConstantExpr;
                                                          
ConstantArray = "[" ConstantExpr { "," ConstantExpr } "]";

UnaryArithOp = "+" | "-"

BinaryArithOp = "+" | "-" | "*" | "/" | "%" | "**";

CompareExpr = IDENTIFIER CmpOp IDENTIFIER
              | IDENTIFIER CmpOp ConstantExpr
              | ConstantExpr CmpOp IDENTIFIER
              | ConstantExpr CmpOpRestricted IDENTIFIER CmpOpRestricted ConstantExpr;

CmpOpRestricted = "<" | "<=";

CmpOp = ">" | ">=" | "<" | "<=" | "=="| "!=";
```

The following table lists the description of each symbol in the above Boolean expression rules.


| **Notation**      | **Description** |
| ----------- | ----------- |
| ,      | Concatenation       |
| ;      | Termination        |
| |      | Alternation       |
| {...}   | Repetition        |
| (...)      | Grouping       |
| NIL   | Empty. The expression can be an empty string.        |
| INTEGER      | Intergers such as 1, 2, 3.       |
| FLOAT   | Float nubmers such as 1.0, 2.0.        |
| CONST      | Intergers or float numbers.       |
| IDENTIFIER   | Identifier. In Milvus, this represents the field name.        |
| LogicalOp      | Logical operators allow the combining of more than one relational test in one comparison. Logical operators return a TRUE (1) or FALSE (0) value. LogicalOp include BinaryLogicalOp and UnaryLogicalOp.       |
| UnaryLogicalOp   | Unary logical operator, "not".        |
| BinaryLogicalOp   | Text        |
| Header      | Binary logical operators that perform actions with two operands. In a complex expression, (two or more operands) the order of evaluation depends on precedence rules.       |
| ArithmeticOp   | Arithmetic operators perform mathematical operations such as addition and subtraction with operands.         |
| UnaryArithOp      | Unary operators are arithmetic operators that perform an action on a single operand.The negative unary operator reverses the sign of an expression from positive to negative or vice versa.       |
| BinaryArithOp   | Binary operators perform actions with two operands. In a complex expression, (two or more operands) the order of evaluation depends on precedence rules.        |
| CmpOp   | Relational operators perform actions with two operands.        |
| CmpOpRestricted      |  Restricted to "Less than" and "Equal".       |
| ConstantExpr   | ConstantExpr can be a Constant or a BinaryArithop on two ConstExpr or an UnaryArithOp on a single ConstantExpr. It is defined recursively.        |
| ConstantArray      | ConstantArray is wrapped with a pair of square brackets, and ConstantExpr can be repeated in the square brackets. ConstArray must include at least 1 ConstantExpr.       |
| TermExpr   | TermExpr is used to check whether the value of an Identifier appears in a ConstantArray. TermExpr is represented by "in".        |
| CompareExpr      | Abbreviation of comparison expression. CompareExpr can be relational operations on two indeifiers, or relational operations on one identifier and one ConstantExpr, or ternary operation performed on two ConstantExprs and one identifier.       |
| SingleExpr   | Single expression. SingleExpr can be TermExpr or CompareExpr.        |
| LogicalExpr      | Logical expression. LogicalExpr can be a BinaryLogicalOp on two LogicalExprs, or an UnaryLogicalOp on a single LogicalExpr or a grouped LogicalExpr or a SingleExpr. It is defined recursively.       |
| Expr   | Abbreviation of expression. Expr can be LogicalExpr or NIL.        |

## Operators

### Logical operators:

| **Symbol**| **Operation** | **Example** | **Description**           |
| ----------| ------------- | ----------- | ------------------------- |
| 'and' &&  | and           | expr1 && expr2   | True if both expr1 and expr2 are true. |
| 'or' \|\|  | or           | expr1 \|\| expr2     | True if either expr1 or expr2 are true.  |



### Binary arithmetic operators:

| **Symbol**| **Operation** | **Example** | **Description**           |
| ----------| ------------- | ----------- | ------------------------- |
| +         | Addition      | a + b       | Add the two operands.     |
| -         | Subtraction   | a - b       | Subtract the second operand from the first operand.  |
| *         | Multiplication| a * b       | Multiply the two operands.     |
| /         | Division      | a / b       | Divide the first operand by the second operand.     |
| **        | Power         | a ** b      | Raise the first operand to the power of the second operand.     |
| %         | Modulo        | a % b       | Divide the first operand by the second operand and yield the remainder portion.    |


### Relational operators:

| **Symbol**| **Operation** | **Example** | **Description**           |
| ----------| ------------- | ----------- | ------------------------- |
| <         | Less than      | a < b      | True if a is less than b.     |
| >         | Greater than   | a > b       | True if a is greater than b.  |
| ==        | Equal          | a == b      | True if a is equal to b.    |
| !=        | Not equal       | a != b     | True if a is not equal to b.     |
| <=        | Less than or equal          | a <= b     | True if a is less than or equal to b.     |
| >=        | Greater than or equal         | a >= b      | True if a is greater than or equal to b.    |


## Operator precedence and associativity

The following table lists the precedence and associativity of operators. Operators are listed top to bottom, in descending precedence.

| Precedence | Operator  | Description   | Associativity |
|------------|-----------|---------------|---------------|
| 1          | + -       | UnaryArithOp  | Left-to-right |
| 2          | not       | UnaryLogicOp  | Right-to-left |
| 3          | **        | BinaryArithOp | Left-to-right |
| 4          | * / %     | BinaryArithOp | Left-to-right |
| 5          | + -       | BinaryArithOp | Left-to-right |
| 6          | < <= > >= | CmpOp         | Left-to-right |
| 7          | == !=     | CmpOp         | Left-to-right |
| 8          | && and    | BinaryLogicOp | Left-to-right |
| 9          | \|\| or     | BinaryLogicOp | Left-to-right |


Expressions are normally evaluated from left to right. Complex expressions are evaluated one at a time. The order in which the expressions are evaluated is determined by the precedence of the operators used. 

If an expression contains two or more operators with the same precedence, the operator to the left is evaluated first. 

<div class="alert note">
For example, 10 / 2 * 5 will be evaluated as (10 / 2) and the result multiplied by 5. 
</div>

When a lower precedence operation should be processed first, it should be enclosed within parentheses. 

<div class="alert note">
For example, 30 / 2 + 8. This is normally evaluated as 30 divided by 2 then 8 added to the result. If you want to divide by 2 + 8, it should be written as 30 / (2 + 8). 
</div>


Parentheses can be nested within expressions. Innermost parenthetical expressions are evaluated first.