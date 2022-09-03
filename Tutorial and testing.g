
# run this just to make things more interesting
ColorPrompt(true);


#locate file to read in, in my case i put it in home directory for ease.
DirectoryContents(DirectoryCurrent());

#see that the desireable file is in the list (in position 20), so will assign it
# this can be done without referring to the item and just pass its name as a string in arg 2 of FileName
readme:= Filename(DirectoryCurrent(),DirectoryContents(DirectoryCurrent())[20]);;

#Then read it in, may be useful to check that permissions exist with 
IsReadableFile(readme);
Read(readme);

#with the functions loaded, you can now use them to generate matrices, some examples below

#setting a seed for consistency
RANDOM_SEED(1);


f := FreeGroup("a1","b1","a2","b2");
AssignGeneratorVariables(f);

# interesting you have to define the genus 2 surface group as such, otherwise it doesnt work
#g := f/[[Comm(a1,b1),Comm(b2,a2)]];
g := f/[Comm(a1,b1)*Comm(a2,b2)];
kb_g := KBMAGRewritingSystem(g);;

# if you were to just knuth bendix with this it would not work, result in a fail and a infinite rules
# however changing the order using below code according to example 6.3 of Knuth bendix on groups.pdf   does work
#KnuthBendix(kb_g);

ReorderAlphabetOfKBMAGRewritingSystem(kb_g, (3,5)(4,6));
KnuthBendix(kb_g);

#treat this as a baseline to keep to the importance of it in the discovery of such things. 
# Also been studied quite well so comparisons against my results are not difficult.

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
		Add(fixed_length, get_reduced_words(g, j, i, kb_g));;
		Add(fixed_length_time_gen, Runtime() - now);;
		
		now := Runtime();;
		big_func(g, j, i, 0.5, kb_g);;
		Add(fixed_length_time_mat, Runtime() - now);;
		
	od;;
	Add(words_matrix, fixed_length);;
	Add(times_matrix_word_generation, fixed_length_time_gen);;
	Add(times_matrix_complete, fixed_length_time_mat);;
od;;


times_matrix_word_metric := [];;
times_matrix_gromov_distance := [];;
times_matrix_visual_metric := [];;

visual_matrices := [];;

for i in words_matrix do
	word_length_time := [];;
	gromo_length_time := [];;
	visual_length_time := [];;
	for j in i do
		now := Runtime();;
		dist_mat_words(kb_g, j);;
		Add(word_length_time, Runtime() - now);
		
		now := Runtime();;
		dist_mat_gromo(kb_g, j);;
		Add(gromo_length_time, Runtime() - now);
		
		now := Runtime();;
		dist_mat(kb_g, j, 0.5);;
		Add(visual_length_time, Runtime() - now);
	od;
	Add(times_matrix_word_metric, word_length_time);;
	Add(times_matrix_gromov_distance, gromo_length_time);;
	Add(times_matrix_visual_metric, visual_length_time);;
od;


name := Filename(DirectoryCurrent( ), "times_matrix_word_generation.csv");
print_mat(times_matrix_word_generation, name);

name := Filename(DirectoryCurrent( ), "times_matrix_complete.csv");
print_mat(times_matrix_complete, name);

name := Filename(DirectoryCurrent( ), "times_matrix_gromov_distance.csv");
print_mat(times_matrix_gromov_distance, name);

name := Filename(DirectoryCurrent( ), "times_matrix_visual_metric.csv");
print_mat(times_matrix_visual_metric, name);

name := Filename(DirectoryCurrent( ), "times_matrix_word_metric.csv");
print_mat(times_matrix_word_metric, name);

