from pyswip import Prolog

prolog= Prolog()

prolog.assertz("father(michael,john)")
prolog.assertz("father(michael,gina)")
print(list(prolog.query("father(michael,X)")) == [{'X': 'john'}, {'X': 'gina'}])