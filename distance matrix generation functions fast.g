

LoadPackage("kbmag");;

# takes input of free group (not neccesarily tbf but is its intention) f
# n = number of words to generate from f
# l = word length to generate (must be a scalar)
get_reduced_words_2:= function(f,n,l)
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

# way faster, bit hackier
get_reduced_words := function(g, n, l)
	local words, kb_g, i, w;
	words := [];
	AssignGeneratorVariables(g);
	kb_g := KBMAGRewritingSystem(g);
	KnuthBendix(kb_g);;
	for i in [1..n*5] do
		w := ReducedForm(kb_g, UnderlyingElement(PseudoRandom(g: radius := l*10)));
		if Length(w) >= l then
			Add(words, Subword(w, 1, l));
		fi;
		if Length(words) = n then
			words:=DuplicateFreeList(words);
		fi;
		if Length(words) = n then
			break;
		fi;
	od;
	return DuplicateFreeList(words);;
end;

# super hacky, super weird, kinda fast
# may not return n amount in specific circumstances, generates n*1.25 randoms but then dedupes them so...
get_free_words := function(f, n, l)
    local words, i;
    AssignGeneratorVariables(f);
    words:=[];
    for i in [1..Int(n*1.25)] do
        Add(words,UnderlyingElement(PseudoRandom(f: radius := l )));
    od;
    words:=DuplicateFreeList(words);;
    words:=List([1..Minimum(Length(words),n)], i->words[i]);;
    return words;;
end;;


# takes input of g = group (already made with relations etc)
# n = number of reduced words to generate
# l = word length of first generated words

# takes the group g, and generates n times random words of length l from the free group of generate
# it then reduced these words 
bryce_func := function(g, n, l)
    local un_words, kb_g, red_words, j;;
    un_words:=get_free_words(g, n*2, l);;
    kb_g:=KBMAGRewritingSystem(g);;
    KnuthBendix(kb_g);;
    red_words:=[];;
    for j in un_words do
        Add(red_words, ReducedForm(kb_g, j));
        red_words:=DuplicateFreeList(red_words);;
        if Length(red_words) = n then
            break;
        fi;
    od;
    return red_words;;
end;;



# can pass group into this as g or knuthbenix on group
# w1 and w2 must be words of group
word_metric := function(g, w1, w2)
    local kb_g;
    if IsKBMAGRewritingSystemRep(g) then
        return Length(ReducedForm(g, w1^-1*w2));;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        return Length(ReducedForm(kb_g, w1^-1*w2));;
    fi;
end;;


# only put in reduced words otherwise may not work in specific (albeit unlikely) cases
# can input a third word to act as the x thingy but if not will use identity
gromov_distance := function(g, w1, w2, w3...)
    local kb_g, id;
    if Length(w3)=0 then
        id := w1^-1*w1;
    else
        id := w3[1];
    fi;
    if w1 = w2 then
        return 1.0/0.0;;
    else
        if IsKBMAGRewritingSystemRep(g) then
            return (word_metric(g, id, w1) + word_metric(g, id, w2) - word_metric(g, w1, w2))*0.5;;
        else
            kb_g:=KBMAGRewritingSystem(g);;
            KnuthBendix(kb_g);;
                return (word_metric(kb_g, id, w1) + word_metric(kb_g, id, w2) - word_metric(kb_g, w1, w2))*0.5;;
        fi;
    fi;
end;

visual_metric := function(grom, eps)
    return Exp(Float(-eps*grom));;
end;;


dist_mat := function(g, words, eps)
    local matrix, i, j, row, gromo, vis, kb_g;
    matrix := [];
    if IsKBMAGRewritingSystemRep(g) then
        for i in words do
            row :=[];
            for j in words do
                gromo := gromov_distance(g, i, j);
                vis := visual_metric(gromo, eps);
                Add(row, vis);
            od;
            Add(matrix, row);
        od;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        for i in words do
            row :=[];
            for j in words do
                gromo := gromov_distance(kb_g, i, j);
                vis := visual_metric(gromo, eps);
                Add(row, vis);
            od;
            Add(matrix, row);
        od;
    fi;
    return matrix;;
end;

dist_mat_gromo := function(g, words)
    local matrix, i, j, row, gromo, kb_g;
    matrix := [];
    if IsKBMAGRewritingSystemRep(g) then
        for i in words do
            row :=[];
            for j in words do
                gromo := gromov_distance(g, i, j);
                Add(row, gromo);
            od;
            Add(matrix, row);
        od;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        for i in words do
            row :=[];
            for j in words do
                gromo := gromov_distance(kb_g, i, j);
                Add(row, gromo);
            od;
            Add(matrix, row);
        od;
    fi;
    return matrix;;
end;

dist_mat_words := function(g, words)
    local matrix, i, j, row, w_met, kb_g;
    matrix := [];
    if IsKBMAGRewritingSystemRep(g) then
        for i in words do
            row :=[];
            for j in words do
                w_met := word_metric(g, i, j);
                Add(row, w_met);
            od;
            Add(matrix, row);
        od;
    else
        kb_g:=KBMAGRewritingSystem(g);;
        KnuthBendix(kb_g);;
        for i in words do
            row :=[];
            for j in words do
                w_met := word_metric(g, i, j);
                Add(row, w_met);
            od;
            Add(matrix, row);
        od;
    fi;
    return matrix;;
end;

MatToRec := function(mat);
	return(rec(1 := mat));;
end;;

MatToRec_not_the_best := function(mat)
	local r, i;
	r := rec();
	for i in mat do
	\.\:\=( r, RNamObj(Position( mat, i)), i );
	od;
	return r;;
end;;


big_func := function(g, n, l, eps)
    local kb_g, words, i, w;
    AssignGeneratorVariables(g);;
    kb_g:=KBMAGRewritingSystem(g);;
    KnuthBendix(kb_g);;
	words:=[];
	for i in [1..n*5] do
		w := ReducedForm(kb_g, UnderlyingElement(PseudoRandom(g: radius := l*10)));
		if Length(w) >= l then
			Add(words, Subword(w, 1, l));
		fi;
		if Length(words) = n then
			words:=DuplicateFreeList(words);
		fi;
		if Length(words) = n then
			break;
		fi;
	od;
	words:=DuplicateFreeList(words);
    return dist_mat(kb_g, words, eps);;
end;;

big_func_rec := function(g, n, l, eps)
	return MatToRec(big_func(g, n, l, eps));;
end;;

#make sure path passed is a working :=Filename()
print_mat := function(mat, path)
	PrintCSV(path, [MatToRec(mat)]);;
end;;

#f:=FreeGroup("a","b");
#AssignGeneratorVariables(f);
#g:=f/[[a^8,b^5, a^0],[a*b^2*a, a]];

#name := Filename(DirectoryCurrent( ), "Small_Mat.csv");
#PrintCSV(name, [rec_mat]);


# surface group, not very good

f := FreeGroup("a1","b1","a2","b2");
AssignGeneratorVariables(f);
g := f/[Comm(a1,b1)*Comm(a2,b2)];
kb_g := KBMAGRewritingSystem(g);
# this step is rediculously slow for this group, idk why, took ages to come up with the rules
KnuthBendix(kb_g);

