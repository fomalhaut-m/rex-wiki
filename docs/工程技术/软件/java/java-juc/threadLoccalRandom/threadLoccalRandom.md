# ThreadLocalRandom

在 Random 类中我们发现 最终实现是一个 AtomicLong 是原子类
这样使用多线程生成的随机数是共享同一个 seed; 在某些场景无法满足需求

```java
    protected int next(int bits) {
        long oldseed, nextseed;
        AtomicLong seed = this.seed;
        do {
            oldseed = seed.get();
            nextseed = (oldseed * multiplier + addend) & mask;
        } while (!seed.compareAndSet(oldseed, nextseed));
        return (int)(nextseed >>> (48 - bits));
    }
```

看 ThreadLocalRandom

首先会根据当前线程 获取一个 随机数实例
```java
    public static ThreadLocalRandom current() {
        if (U.getInt(Thread.currentThread(), PROBE) == 0)
            localInit();
        return instance;
    }
```

获取seed 使用 当前线程的种子, 所以避免了, 多线线程情况下, 得到同一个种子

```java
    @Override
    public int nextInt() {
        return mix32(
                // 获取种子
                nextSeed()
        );
    }

    final long nextSeed() {
        Thread t; long r; // read and update per-thread seed
        U.putLong(t = Thread.currentThread(), SEED,
                  r = U.getLong(t, SEED) + (t.threadId() << 1) + GOLDEN_GAMMA);
        return r;
    }
```