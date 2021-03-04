import matplotlib.pyplot as plt
import tqdm
from lib.loop_gen import *


def loop_only(n):
    rng = np.random.RandomState(0)
    my_loop_generator = LoopGenerator(n, rng, fill_method="lexico")

    my_loop_array = my_loop_generator.generate(axiom_list=[])

    # nasty trick, variable name with several char will be fixed
    # alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    # for i in range(n):
    #     my_loop_array[my_loop_array == str(i)] = alphabet[i]

    my_loop = LoopModel(my_loop_array)
    print(my_loop)
    print("It's a loop :", my_loop.is_loop())

    traj = my_loop_generator.get_trajectory()
    flatten_traj = []
    T = len(traj)

    for k in range(T):
        i, j = traj[k]
        flatten_traj.append(i * n + j)

    plt.figure(figsize=(10, 10))
    for j in range(n):
        plt.plot(np.ones(T) * n * j)

    plt.plot(flatten_traj)
    plt.show()


def iam(n):
    def a(x, y, z):
        s = r"({x}*({y}*{z}))\(({x}*{y})*{z})".format(x=x, y=y, z=z)
        return s

    def K(x, y):
        s = r"({y}*{x})\({x}*{y})".format(x=x, y=y)
        return s

    def T(u, x):
        s = r"({x}\({u}*{x}))".format(x=x, u=u)
        return s

    def L(u, x, y):
        s = r"({y}*{x})\({y}*({x}*{u}))".format(u=u, x=x, y=y)
        return s

    def R(u, x, y):
        s = "(({u}*{x})*{y})/({x}*{y})".format(u=u, x=x, y=y)
        return s

    # AIM axioms :
    identity = '0'
    x, y, z, u, w = 'x', 'y', 'z', 'u', 'w'
    variables = [x, y, z, u, w]

    TT = Axiom(T(T(u, x), y), T(T(u, y), x), variables, "TT")
    TL = Axiom(T(L(u, x, y), z), L(T(u, z), x, y), variables, "TL")
    TR = Axiom(T(R(u, x, y), z), R(T(u, z), x, y), variables, "TR")
    LR = Axiom(L(R(u, x, y), z, w), R(L(u, z, w), x, y), variables, "LR")
    LL = Axiom(L(L(u, x, y), z, w), L(L(u, z, w), x, y), variables, "LL")
    RR = Axiom(R(R(u, x, y), z, w), R(R(u, z, w), x, y), variables, "RR")

    inner_axiom = [TT, TL, TR, LR, LL, RR]

    rng = np.random.RandomState(0)
    my_loop_generator = LoopGenerator(n, rng, fill_method="lexico")

    my_loop_array = my_loop_generator.generate(axiom_list=inner_axiom)

    # nasty trick, variable name with several char will be fixed
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    for i in range(n):
        my_loop_array[my_loop_array == str(i)] = alphabet[i]

    my_loop = LoopModel(my_loop_array)
    print(my_loop)
    print("It's a loop :", my_loop.is_loop())

    for axiom in inner_axiom:
        print(axiom.name, "is", my_loop.is_true(axiom))

    traj = my_loop_generator.get_trajectory()
    flatten_traj = []
    T = len(traj)

    for k in range(T):
        i, j = traj[k]
        flatten_traj.append(i * n + j)

    plt.figure(figsize=(10, 10))
    for j in range(n):
        plt.plot(np.ones(T) * n * j)

    plt.plot(flatten_traj)
    plt.show()


def moufang(n):
    variables = ["x", "y", "z"]
    a1 = Axiom("z*(x*(z*y))", "((z*x)*z)*y", variables)
    a2 = Axiom("x*(z*(y*z))", "((x*z)*y)*z", variables)
    a3 = Axiom("(z*x)*(y*z)", "(z*(x*y))*z", variables)
    a4 = Axiom("(z*x)*(y*z)", "z*((x*y)*z)", variables)

    moufang_axioms = [a1, a2, a3, a4]

    rng = np.random.RandomState(0)
    my_loop_generator = LoopGenerator(n, rng, fill_method="lexico")

    my_loop_array = my_loop_generator.generate(axiom_list=moufang_axioms)

    # nasty trick, variable name with several char will be fixed
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    for i in range(n):
        my_loop_array[my_loop_array == str(i)] = alphabet[i]

    my_loop = LoopModel(my_loop_array)
    print(my_loop)
    print("It's a loop :", my_loop.is_loop())

    for axiom in moufang_axioms:
        print(axiom.name, "is", my_loop.is_true(axiom))

    traj = my_loop_generator.get_trajectory()
    flatten_traj = []
    T = len(traj)

    for k in range(T):
        i, j = traj[k]
        flatten_traj.append(i * n + j)

    plt.figure(figsize=(10, 10))
    for j in range(n):
        plt.plot(np.ones(T) * n * j)

    plt.plot(flatten_traj)
    plt.show()


def gen_loop(N, n, seed=0):
    rng = np.random.RandomState(seed)
    my_loop_generator = LoopGenerator(n, rng, fill_method="lexico")
    my_loop_generator.verbose = False

    PATH = "data/raw/raw_{}/".format(n)
    all_loop = []
    for i in tqdm.tqdm(range(N)):
        my_loop_array = my_loop_generator.generate()
        if my_loop_array.tolist() not in all_loop:
            all_loop.append(my_loop_array.tolist())
        np.savetxt(PATH + "{}.loop".format(i), my_loop_array, fmt="%s")
    # print(len(all_loop))


def gen_moufang(N, n, seed=0):
    variables = ["x", "y", "z"]
    a1 = Axiom("z*(x*(z*y))", "((z*x)*z)*y", variables)
    a2 = Axiom("x*(z*(y*z))", "((x*z)*y)*z", variables)
    a3 = Axiom("(z*x)*(y*z)", "(z*(x*y))*z", variables)
    a4 = Axiom("(z*x)*(y*z)", "z*((x*y)*z)", variables)

    moufang_axioms = [a1, a2, a3, a4]

    rng = np.random.RandomState(seed)
    my_loop_generator = LoopGenerator(n, rng, fill_method="lexico")

    # my_loop_generator.verbose = False

    PATH = "data/moufang/moufang_{}/".format(n)
    all_loop = []
    for _ in tqdm.tqdm(range(N)):
        my_loop_array = my_loop_generator.generate(axiom_list=moufang_axioms)
        if my_loop_array.tolist() not in all_loop:
            all_loop.append(my_loop_array.tolist())

    for i, loop in enumerate(all_loop):
        np.savetxt(PATH + "{}.loop".format(i), loop, fmt="%s")

    print(len(all_loop), " distinct loops over", N)


# gen_moufang(100, 8, seed=2)
gen_loop(10000, 8)
#
# for i in range(13, 20):
#     gen_loop(100, i)

