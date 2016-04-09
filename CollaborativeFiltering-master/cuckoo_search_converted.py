@mfunction("bestnest, fmin")
def cuckoo_search(n=None):
    if nargin < 1:
        # Number of nests (or different solutions)
        n = 25
        end

        # Discovery rate of alien eggs/solutions
        pa = 0.25

        #% Change this if you want to get better results
        # Tolerance
        Tol = 1.0e-5
        #% Simple bounds of the search domain
        # Lower bounds
        nd = 15
        Lb = -5 * ones(1, nd)
        # Upper bounds
        Ub = 5 * ones(1, nd)

        # Random initial solutions
        for i in mslice[1:n]:
            nest(i, mslice[:]).lvalue = Lb + (Ub - Lb) *elmul* rand(size(Lb))
            end

            # Get the current best
            fitness = 10 ** 10 * ones(n, 1)
            [fmin, bestnest, nest, fitness] = get_best_nest(nest, nest, fitness)
            N_iter = 0
#% Starting iterations
while (fmin > Tol):

    # Generate new solutions (but keep the current best)
    new_nest = get_cuckoos(nest, bestnest, Lb, Ub)
    [fnew, best, nest, fitness] = get_best_nest(nest, new_nest, fitness)
    # Update the counter
    N_iter = N_iter + n
    # Discovery and randomization
    new_nest = empty_nests(nest, Lb, Ub, pa)

    # Evaluate this set of solutions
    [fnew, best, nest, fitness] = get_best_nest(nest, new_nest, fitness)
    # Update the counter again
    N_iter = N_iter + n
    # Find the best objective so far  
    if fnew < fmin:
        fmin = fnew
        bestnest = best
        end
        end    #% End of iterations

        #% Post-optimization processing
        #% Display all the nests
        disp(strcat(mstring('Total number of iterations='), num2str(N_iter)))
        fmin()
        bestnest()

        #% --------------- All subfunctions are list below ------------------
        #% Get cuckoos by ramdom walk
@mfunction("nest")
def get_cuckoos(nest=None, best=None, Lb=None, Ub=None):
    # Levy flights
    n = size(nest, 1)

    beta = 3 / 2
    sigma = (gamma(1 + beta) * sin(pi * beta / 2) / (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)

    for j in mslice[1:n]:
        s = nest(j, mslice[:])

        u = randn(size(s)) * sigma
        v = randn(size(s))
        step = u /eldiv/ abs(v) **elpow** (1 / beta)

        stepsize = 0.01 * step *elmul* (s - best)

        s = s + stepsize *elmul* randn(size(s))
        # Apply simple bounds/limits
        nest(j, mslice[:]).lvalue = simplebounds(s, Lb, Ub)
        end

        #% Find the current best nest
        [fmin, K] = min(fitness)
best = nest(K, mslice[:])

#% Replace some nests by constructing new solutions/nests
@mfunction("new_nest")
def empty_nests(nest=None, Lb=None, Ub=None, pa=None):
    # A fraction of worse nests are discovered with a probability pa
    n = size(nest, 1)
    # Discovered or not -- a status vector
    K = rand(size(nest)) > pa


    stepsize = rand * (nest(randperm(n), mslice[:]) - nest(randperm(n), mslice[:]))
    new_nest = nest + stepsize *elmul* K
    for j in mslice[1:size(new_nest, 1)]:
        s = new_nest(j, mslice[:])
        new_nest(j, mslice[:]).lvalue = simplebounds(s, Lb, Ub)
        end
        # Application of simple constraints
@mfunction("s")
def simplebounds(s=None, Lb=None, Ub=None):
    # Apply the lower bound
    ns_tmp = s
    I = ns_tmp < Lb
    ns_tmp(I).lvalue = Lb(I)

    # Apply the upper bounds 
    J = ns_tmp > Ub
    ns_tmp(J).lvalue = Ub(J)
    # Update this new move 
    s = ns_tmp


@mfunction("z")
def fobj(u=None):

    z = sum((u - 1) **elpow** 2)