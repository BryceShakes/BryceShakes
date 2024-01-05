

LoadPackage("kbmag");;

# g = input of group
# n = number of words to generate from g
# l = length of these words
# rws = optional entry where you can pass an already confluent system, for cases when the default knuth bendix routine on g doesnt work (must already be confluent)
# this is a fast way of generating reduced words on a sphere
# it generates a random word in the free group, larger than l, reduces it according to the knuth bendix and returns subword of length l of the reduced word (if possible)
# is a lot faster as it does not require generation of all words which for large l is not feasible
# if n is greater than the number of words of length l however it will keep trying to generate more, until it has tried a total of 5n times
GetReducedWords := function(g, n, l, rws...)
	local words, kb_g, i, w;
	words := [];;
	AssignGeneratorVariables(g);;
	if Length(rws) = 0 then
		kb_g := KBMAGRewritingSystem(g);;
		KnuthBendix(kb_g);;
	else 
		kb_g := rws[1];;
	fi;
	for i in [1..n*5] do
		w := ReducedForm(kb_g, UnderlyingElement(PseudoRandom(g: radius := l*5)));;
		if Length(w) >= l then
			Add(words, Subword(w, 1, l));;
		fi;
		if Length(words) = n then
			words:=DuplicateFreeList(words);;
		fi;
		if Length(words) = n then
			break;;
		fi;
	od;
	return DuplicateFreeList(words);;
end;


# f = input of group 
# n = number of words to generate from f
# l = word length to generate (must be a scalar)
# this works by generating all elements whose words freely reduced words have length l
# then selecting randomly from these elements
# this is a very slow way of generating points on a sphere for a group, would not reccomend unless you want points from a very small group
# in this case its recommended as first generates all points in that sphere, so terminates once there are no unique points left (even if n is not met yet)
GetReducedWords2:= function(f,n,l)
    local kb_f, rando, words, points, pos, i;
    rando:=RandomSource(IsMersenneTwister, 42);
    if IsKBMAGRewritingSystemRep(f) then
        words:=EnumerateReducedWords(f,l,l);
        points:=[];
        for i in [1..n] do
            pos := Random(rando,1,Length(words));
            Add(points, words[pos]);
            Remove(words, pos);
            if Length(words) = 0 then
                break;
            fi;
        od;
    else
        kb_f:=KBMAGRewritingSystem(f);
        KnuthBendix(kb_f);;
        words:=EnumerateReducedWords(kb_f,l,l);
        points:=[];
        for i in [1..n] do
            pos := Random(rando,1,Length(words));
            Add(points, words[pos]);
            Remove(words, pos);
            if Length(words) = 0 then
                break;
            fi;
        od;
    fi;
    Unbind(words);
    return points;;
end;


# f = input of group, words generated are from underlying free group
# n = number of words to generate from free group of f
# l = length of these words
# generates n*1.25 words of length l, dedupes and returns n remaining words
# this assumes you are generating free words of a large radius so the dedupe does not remove more than 0.25*n
# very fast for generating lots of long free words
GetFreeWords := function(f, n, l)
    local words, i;
    AssignGeneratorVariables(f);;
    words:=[];;
    for i in [1..Int(n*1.25)] do
        Add(words,UnderlyingElement(PseudoRandom(f: radius := l )));;
    od;
    words:=DuplicateFreeList(words);;
    words:=List([1..Minimum(Length(words),n)], i->words[i]);;
    return words;;
end;;


# g = input of group
# n = number of words to generate
# l = length of words before reduction
# rws = optional entry where you can pass an already confluent system, for cases when the default knuth bendix routine on g doesnt work (must already be confluent)
# takes the group g, and generates n times random words of length l from its underlying free group using above function
# it then reduces these words according to the rules of g and returns them
# interesting for seeing where reduction occurs although not used in my work
# this assumes you are generating free words of a large radius so the dedupe does not remove too many
GetReducedFreeWords := function(g, n, l)
    local un_words, kb_g, red_words, j;;
    un_words:= GetFreeWords(g, n*2, l);;
	if IsKBMAGRewritingSystemRep(g) then
		kb_g := g;;
	else
		kb_g:=KBMAGRewritingSystem(g);;
		KnuthBendix(kb_g);;
	fi;;
    red_words:=[];;
    for j in un_words do
        Add(red_words, ReducedForm(kb_g, j));;
        if Length(red_words) = n then
			red_words:=DuplicateFreeList(red_words);;
		fi;
		if Length(red_words) = n then
            break;
        fi;
    od;
    return red_words;;
end;;



# g = input of group or already confluent RWS (if the former will produce standard knuthbendix, if latter will use the rules passed)
# w1,w2 = a word representing an element in g
# returns the word_length of w1^-1*w2 according to the knuth bendix, even if w1 and w2 are not in normal form, output will be.
WordMetric := function(g, w1, w2)
    local kb_g;
    if IsKBMAGRewritingSystemRep(g) then
        return Length(ReducedForm(g, (w1^-1)*w2));;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        return Length(ReducedForm(kb_g, (w1^-1)*w2));;
    fi;
end;;


# g = input of group or already confluent RWS (if the former will produce standard knuthbendix, if latter will use the rules passed)
# w1,w2 = a word representing an element in g
# w3 = optional base point, default is the identity
# returns the gromov product of w1 and w2 at w3
# even if inputs are not of normal form, will take the most reduced version of w1,2,3 according to the rules of g
GromovProduct := function(g, w1, w2, w3...)
    local kb_g, id;
    if Length(w3)=0 then
        id := w1^-1*w1;;
    else
        id := w3[1];;
    fi;
    if w1 = w2 then
        return 1.0/0.0;;
    else
        if IsKBMAGRewritingSystemRep(g) then
            return (WordMetric(g, id, w1) + WordMetric(g, id, w2) - WordMetric(g, w1, w2))*0.5;;
        else
            kb_g:=KBMAGRewritingSystem(g);;
            KnuthBendix(kb_g);;
                return (WordMetric(kb_g, id, w1) + WordMetric(kb_g, id, w2) - WordMetric(kb_g, w1, w2))*0.5;;
        fi;
    fi;
end;

# grom = gromov product (or any integer)
# eps = number > 0
# returns e^(-eps * gromo), according to boundary for hyperbolic group
VisualMetric := function(grom, eps)
    return Exp(Float(-eps*grom));;
end;;

# g = input of group or already confluent RWS (if the former will produce standard knuthbendix, if latter will use the rules passed)
# words = list of words in the generating set of g
# eps = number >0
# given a list of words returns the dissimilarity matrix where Dij = VisualMetric(GromovProduct(g, i, j), eps)
# note that default base point of the gromov product is always the identity
VisualMatrix := function(g, words, eps)
    local matrix, i, j, row, gromo, vis, kb_g;
    matrix := [];;
    if IsKBMAGRewritingSystemRep(g) then
        for i in words do
            row :=[];;
            for j in words do
                vis := VisualMetric(GromovProduct(g, i, j), eps);;
                Add(row, vis);;
            od;
            Add(matrix, row);;
        od;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        for i in words do
            row :=[];
            for j in words do
                vis := VisualMetric(GromovProduct(g, i, j), eps);;
                Add(row, vis);;
            od;
            Add(matrix, row);;
        od;
    fi;
    return matrix;;
end;

# g = input of group or already confluent RWS (if the former will produce standard knuthbendix, if latter will use the rules passed)
# words = list of words in the generating set of g
# given a list of words returns the dissimilarity matrix where Dij = GromovProduct(g, i, j)
# note that default base point of the gromov product is always the identity
GromovProductMatrix := function(g, words)
    local matrix, i, j, row, gromo, kb_g;
    matrix := [];;
    if IsKBMAGRewritingSystemRep(g) then
        for i in words do
            row :=[];;
            for j in words do
                gromo := GromovProduct(g, i, j);;
                Add(row, gromo);;
            od;
            Add(matrix, row);;
        od;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        for i in words do
            row :=[];;
            for j in words do
                gromo := GromovProduct(kb_g, i, j);;
                Add(row, gromo);;
            od;
            Add(matrix, row);;
        od;
    fi;
    return matrix;;
end;

# g = input of group or already confluent RWS (if the former will produce standard knuthbendix, if latter will use the rules passed)
# words = list of words in the generating set of g
# given a list of words returns the dissimilarity matrix where Dij = WordMetric(g, i, j)
WordMetricMatrix := function(g, words)
    local matrix, i, j, row, w_met, kb_g;
    matrix := [];;
    if IsKBMAGRewritingSystemRep(g) then
        for i in words do
            row :=[];;
            for j in words do
                w_met := WordMetric(g, i, j);;
                Add(row, w_met);;
            od;
            Add(matrix, row);;
        od;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        for i in words do
            row :=[];;
            for j in words do
                w_met := WordMetric(g, i, j);;
                Add(row, w_met);;
            od;
            Add(matrix, row);;
        od;
    fi;
    return matrix;;
end;

# g = input of group
# n = number of words to generate from g
# l = length of these words
# eps = number > 0
# rws = optional entry where you can pass an already confluent system, for cases when the default knuth bendix routine on g doesnt work 
# generates n words in a list (the list is called words) of length l representing elements in g, same method as get_reduced_words
# then returns the matrix by doing VisualMatrix(g, words, eps). this takes into account the optional argument RWS for g as in the VisualMatrix functions
GetVisualMatrix := function(g, n, l, eps, rws...)
    local kb_g, words, i, w;
    AssignGeneratorVariables(g);;
	if Length(rws) = 0 then
		kb_g:=KBMAGRewritingSystem(g);;
		KnuthBendix(kb_g);;
	else
		kb_g := rws[1];;
	fi;
	words:=[];
	for i in [1..n*5] do
		w := ReducedForm(kb_g, UnderlyingElement(PseudoRandom(g: radius := l*10)));;
		if Length(w) >= l then
			Add(words, Subword(w, 1, l));;
		fi;
		if Length(words) = n then
			words:=DuplicateFreeList(words);;
		fi;
		if Length(words) = n then
			break;
		fi;
	od;
	words:=DuplicateFreeList(words);;
    return VisualMatrix(kb_g, words, eps);;
end;;

# mat = matrix or list
# printing to csv in GAP is messy as far as i can tell, the second argument of PrintCSV requiring a list of records
# this function takes the input mat (presumably from a -----Matrix function) and returns the record which can then be used to print it
MatToRec := function(mat);
	return(rec(1 := mat));;
end;;

# very similar to MatToRec, returns the record of the input, but each row is a separate entry
MatToRec2 := function(mat)
	local r, i;
	r := rec();;
	for i in mat do
	\.\:\=( r, RNamObj(Position( mat, i)), i );;
	od;
	return r;;
end;;

# g = input of group
# n = number of words to generate from g
# l = length of these words
# eps = number > 0
# generates n words in a list (the list is called words) of length l representing elements in g, same method as get_reduced_words
# generates a matrix by doing VisualMatrix(g, words, eps)
# returns MatToRec of this matrix
# note that this does not account for an optional input of RWS like VisualMatrix does
GetVisualMatrixRec := function(g, n, l, eps)
	return MatToRec(GetVisualMatrix(g, n, l, eps));;
end;;


# mat = matrix or list
# path = a FileName() object, dictating the csv location and name
# my recommended way to use PrintCSV so that the python code can interpret it, once again PrintCSV is messy.
# Once again printing is messy, this function takes an input (mat) and desired location (name) and produces a csv of mat at name
# This forces the csv to print the matrix in a way that the python code can then interpet (although the python code can also interpet doing PrintCSV on mattorec and MatToRec_not_the_best objects also)
PrintMatrix := function(mat, path)
	PrintCSV(path, [MatToRec(mat)]);;
end;;



