
##########################
#	preliminaries
##########################

# run this just to make things more interesting
ColorPrompt(true);

# useful package to have especially for use
# https://mate.dm.uba.ar/~isadofschi/smallcancellation/chap0_mj.html
LoadPackage("smallcancellation");

#locate file to read in, in my case i put it in home directory for ease.
DirectoryContents(DirectoryCurrent());

#see that the desireable file is in the list (in position 20), so will assign it
# this can be done without referring to the item and just pass its name as a string in arg 2 of FileName
readme:= Filename(DirectoryCurrent(),DirectoryContents(DirectoryCurrent())[20]);

#Then read it in, may be useful to check that permissions exist with 
IsReadableFile(readme);
Read(readme);

#with the functions loaded, you can now use them to generate matrices, some examples below

#setting a seed for consistency
RANDOM_SEED(1);


##########################
#	setting up genus-2
##########################

f := FreeGroup("a1","b1","a2","b2");
AssignGeneratorVariables(f);

#g := f/[[Comm(a1,b1),Comm(b2,a2)]];
g := f/[Comm(a1,b1)*Comm(a2,b2)];
kb_g := KBMAGRewritingSystem(g);;

# if you were to just knuth bendix with this it would not work, result in a fail and a infinite rules
# however changing the order using below code according to example 6.3 of https://www.sciencedirect.com/science/article/pii/S0747717108800934 does work
ReorderAlphabetOfKBMAGRewritingSystem(kb_g, (3,5)(4,6));
KnuthBendix(kb_g);

# this will work regardless of ordering although is exceptionally slow
# AutomaticStructure(kb_g);


#treat this as a baseline to keep to the importance of it in the discovery of such things. 
# Also been studied quite well so comparisons against my results are not difficult.


##########################
#	Time Testing
##########################

tests := [10,100,1000];;

words_matrix := [];;
times_matrix_word_generation := [];;
times_matrix_complete := [];;

for i in tests do
	fixed_length := [];;
	fixed_length_time_gen := [];;
	fixed_length_time_mat := [];; 
	for j in tests do
		now := Runtime();;
		# passing optional argument through here for RWS as we have altered the default reqriting system to make it work
		Add(fixed_length, GetReducedWords(g, j, i, kb_g));;
		Add(fixed_length_time_gen, Runtime() - now);;
		
		now := Runtime();;
		GetVisualMatrix(g, j, i, 0.5, kb_g);;
		Add(fixed_length_time_mat, Runtime() - now);;
		
	od;;
	Add(words_matrix, fixed_length);;
	Add(times_matrix_word_generation, fixed_length_time_gen);;
	Add(times_matrix_complete, fixed_length_time_mat);;
od;;


times_matrix_WordMetric := [];;
times_matrix_GromovProduct := [];;
times_matrix_VisualMetric := [];;

visual_matrices := [];;

for i in words_matrix do
	word_length_time := [];;
	gromo_length_time := [];;
	visual_length_time := [];;
	for j in i do
		now := Runtime();;
		VisualMatrix_words(kb_g, j);;
		Add(word_length_time, Runtime() - now);
		
		now := Runtime();;
		VisualMatrix_gromo(kb_g, j);;
		Add(gromo_length_time, Runtime() - now);
		
		now := Runtime();;
		VisualMatrix(kb_g, j, 0.5);;
		Add(visual_length_time, Runtime() - now);
	od;
	Add(times_matrix_WordMetric, word_length_time);;
	Add(times_matrix_GromovProduct, gromo_length_time);;
	Add(times_matrix_VisualMetric, visual_length_time);;
od;


name := Filename(DirectoryCurrent( ), "times_matrix_word_generation.csv");
PrintMatrix(times_matrix_word_generation, name);

name := Filename(DirectoryCurrent( ), "times_matrix_complete.csv");
PrintMatrix(times_matrix_complete, name);

name := Filename(DirectoryCurrent( ), "times_matrix_GromovProduct.csv");
PrintMatrix(times_matrix_GromovProduct, name);

name := Filename(DirectoryCurrent( ), "times_matrix_VisualMetric.csv");
PrintMatrix(times_matrix_VisualMetric, name);

name := Filename(DirectoryCurrent( ), "times_matrix_WordMetric.csv");
PrintMatrix(times_matrix_WordMetric, name);


##########################
#	Testing multiple groups
##########################


f := FreeGroup("a","b");
AssignGeneratorVariables(f);
rels := [(a*b)*(a*b^2)*(a*b^3)*(a*b^4)*(a*b^5)*(a*b^6)*(a*b^7)*(a*b^8)*(a*b^9)*(a*b^10)*(a*b^11)*(a*b^12)*(a*b^13)*(a*b^14)*(a*b^15)*(a*b^16)*(a*b^17)*(a*b^18)*(a*b^19)*(a*b^20)];
g:= f/rels;
GroupSatisfiesCPrime(g, 1/6, true );

SetInfoLevel(InfoRWS, 2);
kb_g := KBMAGRewritingSystem(g);;
ReorderAlphabetOfKBMAGRewritingSystem(kb_g, (1,2,4,3));
# this results in failure
AutomaticStructure(kb_g);


# group referenced in strebel
f := FreeGroup("a","b","c","d");
AssignGeneratorVariables(f);

rels := [a^2*b^2*c^2*d^2];
g:= f/rels;

GroupSatisfiesCPrime(g, 1/6, true );
kb_g := KBMAGRewritingSystem(g);;
AutomaticStructure(kb_g);

strebel := GetVisualMatrix(g, 250, 300, 0.25, kb_g);;
PrintMatrix (strebel, Filename(DirectoryCurrent( ), "strebel.csv"));


# the bryce group - i do not lay claim to this, someone almost certainly came up with it before me
f := FreeGroup("a","b","c","d");
AssignGeneratorVariables(f);
rels := [a^2*b^2*c^2*d*a^-2*b^-2*c^-2, b^2*d^2*a^2*c*b^-2*d^-2*a^-2];
g := f/rels;
GroupSatisfiesC(g, 1/6 );
kb_g := KBMAGRewritingSystem(g);;
#KnuthBendix(kb_g); this fails :( 

ReorderAlphabetOfKBMAGRewritingSystem(kb_g, (3,5)(4,6));
# KnuthBendix(kb_g); this also fails :(

kb_g := KBMAGRewritingSystem(g);;
AutomaticStructure(kb_g);

bryce := GetVisualMatrix(g, 250, 300, 0.25, kb_g);;
PrintMatrix (bryce, Filename(DirectoryCurrent( ), "bryce.csv"));

##########################
#	Not C'(1/6) groups
##########################

f := FreeGroup("a","b");
AssignGeneratorVariables(f);

rels := [a^2, (a*b)^2];
g:= f/rels;
kb_g := KBMAGRewritingSystem(g);;
KnuthBendix(kb_g);

#slightly different approach due to much  smaller group
# in fact there are only 4 points, luckily GetReducedWords2 knows this
words := GetReducedWords2(kb_g, 100,300);
dihedral := VisualMatrix(kb_g, words, 0.25);;
PrintMatrix (dihedral, Filename(DirectoryCurrent( ), "dihedral.csv"));



f := FreeGroup("a","b","c");
AssignGeneratorVariables(f);

rels := [Comm(a,b),Comm(a,c), Comm(a,c)];
g:= f/rels;
kb_g := KBMAGRewritingSystem(g);;
KnuthBendix(kb_g);
z3 := GetVisualMatrix(g, 500, 300, 0.25, kb_g);;
PrintMatrix (z3, Filename(DirectoryCurrent( ), "z3.csv"));