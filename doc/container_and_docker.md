## What is container

Why it confusing between *Docker* and *Container*?

### Definition
Linux containers - Opensource Group
> Linux containers are technologies that allow you to package and isolate applications with their entire runtime environment—all of the files necessary to run. - [linux containers](https://linuxcontainers.org)

Understanding Linux containers - Redhat
> A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. - [what is docker - redhat](https://www.redhat.com/en/topics/containers/what-is-docker)


Containers 101: What are containers? - Google
> Containers offer a logical packaging mechanism in which applications can be abstracted from the environment in which they actually run. - [What are containers?](https://cloud.google.com/containers)

**Container is a technical concept of software aimed to enhance package, delivery and isolating runtime environment. Docker is one of implementation of container concept, it would be just familiar with the field engineers due to using widely.**

### Comparing implementation of containerization
1. JVM (in my opinion)
- *portable runtime environment* - it allows to make easy to deliver a software
- *allocating amount of memory space per JVM* - it would be a kind of resource isolation

2. LXC

    LXC is a userspace interface for the **Linux kernel containment features**.

    #### kernel features in use
    - Kernel namespaces (ipc, uts, mount, pid, network and user): ***partitions*** kernel resources
    - Apparmor and SELinux profiles: kernel security module that allows the system admin to restrict programs' capabilities with ***per-program*** profiles
    - Seccomp policies: it does not virtualize the system's resources but ***isolates the process*** from them entirely
    - Chroots (using pivot_root): change root (directory), it makes each process can have ***isolated*** filesystem
    - Kernel capabilities: distinct unit of super users ***privileges***
    - CGroups (control groups): features that limits, accounts for, and ***isolates*** the resource usage(CPU,memory,diskI/O,network,etc.)

    The thing to keep in mind is that it tends to orient maintaining with Linux upstream in contrast to Docker's.

    ![](https://www.redhat.com/cms/managed-files/what-is-a-container.png)

3. Docker

    Docker have implemented own technologies to realize containerization. Intuitive interface for the developers, (reusable & runnable) layered images, and etc.

    While LXC have been being on the track of Linux upstream, Docker have got the 'ENGINE' to provide the way to run container in anywhere consistently on any infrastructure.

    ![](https://www.redhat.com/cms/managed-files/traditional-linux-containers-vs-docker_0.png)

### Conclusion

The technology concept of containerization and its implementation have been evolving. It's about utilizing resources efficiently and to delivering runnable software effectively. For now, I think, Docker is the good one to adopt our development pipeline. Understanding concept of container and under the hood of Docker would help you to use properly.
