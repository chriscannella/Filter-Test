
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "left+-left*/rightUMINUSNAME NUMBER STRING ASSIGN EQ NEQ GEQ LEQ SG SL BOOL FILTERON OBSERVATION FOR WHILE IN TESTstatementlist : statementlist statementblock\n                     | statementblock statementblock : '{' statementlist '}'\n                      | WHILE '(' expression ')' '{' statementblock '}'\n                      | FOR '(' expression ';' expression ';' expression ')' '{' statementblock '}'\n                      | FOR NAME IN expression '{' statementblock '}' \n                      | statement ';' statement : FILTERON expressionstatement : expressionexpression : expression '+' expression\n                  | expression '-' expression\n                  | expression '*' expression\n                  | expression '/' expression\n                  | expression IN expression\n                  | expression EQ expression\n                  | expression NEQ expression\n                  | expression GEQ expression\n                  | expression LEQ expression\n                  | expression SG expression\n                  | expression SL expressionexpression : '-' expression %prec UMINUSexpression : '(' expression ')'expression : expression '[' expression ']'expression : BOOLexpression : NUMBERexpression : STRINGexpression : OBSERVATIONexpression : NAME ASSIGN expressionexpression : NAMEexpression : TEST"
    
_lr_action_items = {'FILTERON':([0,3,10,15,18,22,26,44,61,62,67,68,71,73,],[1,1,-2,1,-1,-7,1,-3,1,1,-4,-6,1,-5,]),'NUMBER':([0,1,3,5,6,10,15,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,44,59,61,62,66,67,68,71,73,],[2,2,2,2,2,-2,2,-1,2,-7,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,-3,2,2,2,2,-4,-6,2,-5,]),'WHILE':([0,3,10,15,18,22,26,44,61,62,67,68,71,73,],[4,4,-2,4,-1,-7,4,-3,4,4,-4,-6,4,-5,]),'OBSERVATION':([0,1,3,5,6,10,15,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,44,59,61,62,66,67,68,71,73,],[12,12,12,12,12,-2,12,-1,12,-7,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,-3,12,12,12,12,-4,-6,12,-5,]),'GEQ':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,27,27,27,-21,27,-22,27,27,27,27,27,-10,-12,-11,-13,27,27,27,27,27,27,-23,27,27,]),')':([2,8,11,12,13,14,20,21,39,40,43,45,46,47,48,49,50,51,52,53,54,56,60,69,],[-25,-26,-29,-27,-24,-30,40,-21,57,-22,-28,-17,-20,-15,-10,-12,-11,-13,-18,-14,-19,-16,-23,70,]),'(':([0,1,3,4,5,6,9,10,15,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,44,59,61,62,66,67,68,71,73,],[5,5,5,19,5,5,24,-2,5,-1,5,-7,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,-3,5,5,5,5,-4,-6,5,-5,]),'+':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,30,30,30,-21,30,-22,30,30,30,30,30,-10,-12,-11,-13,30,30,30,30,30,30,-23,30,30,]),'*':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,31,31,31,-21,31,-22,31,31,31,31,31,31,-12,31,-13,31,31,31,31,31,31,-23,31,31,]),'-':([0,1,2,3,5,6,8,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,63,66,67,68,69,71,73,],[6,6,-25,6,6,6,-26,-2,-29,-27,-24,-30,6,32,32,-1,6,32,-21,-7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,32,-22,6,32,32,-3,32,32,32,-10,-12,-11,-13,32,32,32,32,32,32,6,-23,6,6,32,6,-4,-6,32,6,-5,]),'/':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,33,33,33,-21,33,-22,33,33,33,33,33,33,-12,33,-13,33,33,33,33,33,33,-23,33,33,]),';':([2,7,8,11,12,13,14,16,17,21,40,42,43,45,46,47,48,49,50,51,52,53,54,56,60,63,],[-25,22,-26,-29,-27,-24,-30,-9,-8,-21,-22,59,-28,-17,-20,-15,-10,-12,-11,-13,-18,-14,-19,-16,-23,66,]),'NEQ':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,38,38,38,-21,38,-22,38,38,38,38,38,-10,-12,-11,-13,38,38,38,38,38,38,-23,38,38,]),'ASSIGN':([11,],[25,]),'$end':([3,10,18,22,44,67,68,73,],[0,-2,-1,-7,-3,-4,-6,-5,]),'STRING':([0,1,3,5,6,10,15,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,44,59,61,62,66,67,68,71,73,],[8,8,8,8,8,-2,8,-1,8,-7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,-3,8,8,8,8,-4,-6,8,-5,]),'FOR':([0,3,10,15,18,22,26,44,61,62,67,68,71,73,],[9,9,-2,9,-1,-7,9,-3,9,9,-4,-6,9,-5,]),'IN':([2,8,11,12,13,14,16,17,20,21,23,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,35,35,35,-21,41,35,-22,35,35,35,35,35,-10,-12,-11,-13,35,35,35,35,35,35,-23,35,35,]),'[':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,37,37,37,-21,37,-22,37,37,37,37,37,-10,-12,-11,-13,37,37,37,37,37,37,-23,37,37,]),']':([2,8,11,12,13,14,21,40,43,45,46,47,48,49,50,51,52,53,54,55,56,60,],[-25,-26,-29,-27,-24,-30,-21,-22,-28,-17,-20,-15,-10,-12,-11,-13,-18,-14,-19,60,-16,-23,]),'EQ':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,29,29,29,-21,29,-22,29,29,29,29,29,-10,-12,-11,-13,29,29,29,29,29,29,-23,29,29,]),'NAME':([0,1,3,5,6,9,10,15,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,44,59,61,62,66,67,68,71,73,],[11,11,11,11,11,23,-2,11,-1,11,-7,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,-3,11,11,11,11,-4,-6,11,-5,]),'}':([10,18,22,26,44,64,65,67,68,72,73,],[-2,-1,-7,44,-3,67,68,-4,-6,73,-5,]),'LEQ':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,34,34,34,-21,34,-22,34,34,34,34,34,-10,-12,-11,-13,34,34,34,34,34,34,-23,34,34,]),'BOOL':([0,1,3,5,6,10,15,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,44,59,61,62,66,67,68,71,73,],[13,13,13,13,13,-2,13,-1,13,-7,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,-3,13,13,13,13,-4,-6,13,-5,]),'SL':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,28,28,28,-21,28,-22,28,28,28,28,28,-10,-12,-11,-13,28,28,28,28,28,28,-23,28,28,]),'TEST':([0,1,3,5,6,10,15,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,44,59,61,62,66,67,68,71,73,],[14,14,14,14,14,-2,14,-1,14,-7,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,-3,14,14,14,14,-4,-6,14,-5,]),'{':([0,2,3,8,10,11,12,13,14,15,18,21,22,26,40,43,44,45,46,47,48,49,50,51,52,53,54,56,57,58,60,61,62,67,68,70,71,73,],[15,-25,15,-26,-2,-29,-27,-24,-30,15,-1,-21,-7,15,-22,-28,-3,-17,-20,-15,-10,-12,-11,-13,-18,-14,-19,-16,61,62,-23,15,15,-4,-6,71,15,-5,]),'SG':([2,8,11,12,13,14,16,17,20,21,39,40,42,43,45,46,47,48,49,50,51,52,53,54,55,56,58,60,63,69,],[-25,-26,-29,-27,-24,-30,36,36,36,-21,36,-22,36,36,36,36,36,-10,-12,-11,-13,36,36,36,36,36,36,-23,36,36,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statementblock':([0,3,15,26,61,62,71,],[10,18,10,18,64,65,72,]),'expression':([0,1,3,5,6,15,19,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,59,61,62,66,71,],[16,17,16,20,21,16,39,42,43,16,45,46,47,48,49,50,51,52,53,54,55,56,58,63,16,16,69,16,]),'statement':([0,3,15,26,61,62,71,],[7,7,7,7,7,7,7,]),'statementlist':([0,15,],[3,26,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statementlist","S'",1,None,None,None),
  ('statementlist -> statementlist statementblock','statementlist',2,'p_statementlist_statementblock','filterparse.py',13),
  ('statementlist -> statementblock','statementlist',1,'p_statementlist_statementblock','filterparse.py',14),
  ('statementblock -> { statementlist }','statementblock',3,'p_statementblock_statement','filterparse.py',21),
  ('statementblock -> WHILE ( expression ) { statementblock }','statementblock',7,'p_statementblock_statement','filterparse.py',22),
  ('statementblock -> FOR ( expression ; expression ; expression ) { statementblock }','statementblock',11,'p_statementblock_statement','filterparse.py',23),
  ('statementblock -> FOR NAME IN expression { statementblock }','statementblock',7,'p_statementblock_statement','filterparse.py',24),
  ('statementblock -> statement ;','statementblock',2,'p_statementblock_statement','filterparse.py',25),
  ('statement -> FILTERON expression','statement',2,'p_statement_filteron','filterparse.py',40),
  ('statement -> expression','statement',1,'p_statement_expr','filterparse.py',44),
  ('expression -> expression + expression','expression',3,'p_expression_binop','filterparse.py',48),
  ('expression -> expression - expression','expression',3,'p_expression_binop','filterparse.py',49),
  ('expression -> expression * expression','expression',3,'p_expression_binop','filterparse.py',50),
  ('expression -> expression / expression','expression',3,'p_expression_binop','filterparse.py',51),
  ('expression -> expression IN expression','expression',3,'p_expression_binop','filterparse.py',52),
  ('expression -> expression EQ expression','expression',3,'p_expression_binop','filterparse.py',53),
  ('expression -> expression NEQ expression','expression',3,'p_expression_binop','filterparse.py',54),
  ('expression -> expression GEQ expression','expression',3,'p_expression_binop','filterparse.py',55),
  ('expression -> expression LEQ expression','expression',3,'p_expression_binop','filterparse.py',56),
  ('expression -> expression SG expression','expression',3,'p_expression_binop','filterparse.py',57),
  ('expression -> expression SL expression','expression',3,'p_expression_binop','filterparse.py',58),
  ('expression -> - expression','expression',2,'p_expression_uminus','filterparse.py',83),
  ('expression -> ( expression )','expression',3,'p_expression_group','filterparse.py',87),
  ('expression -> expression [ expression ]','expression',4,'p_expression_field','filterparse.py',91),
  ('expression -> BOOL','expression',1,'p_expression_bool','filterparse.py',95),
  ('expression -> NUMBER','expression',1,'p_expression_number','filterparse.py',99),
  ('expression -> STRING','expression',1,'p_expression_string','filterparse.py',103),
  ('expression -> OBSERVATION','expression',1,'p_expression_observation','filterparse.py',107),
  ('expression -> NAME ASSIGN expression','expression',3,'p_expression_assign','filterparse.py',111),
  ('expression -> NAME','expression',1,'p_expression_name','filterparse.py',116),
  ('expression -> TEST','expression',1,'p_expression_test','filterparse.py',120),
]
