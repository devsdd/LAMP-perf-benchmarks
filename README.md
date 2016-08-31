## LAMP-perf-benchmarks
Automation using scripts and a Puppet Manifest to install LAMP Packages and run benchmarks to estimate the performance of each component.

### NOTE
This was written for the use case of benchmarking the performance of the LAMP stack on hundreds of KVM virtual machines in parallel. It contains some KVM specific stuff (like disk formats). For a more generic use case one can remove the KVM specific stuff and use it.

## Usage Instructions:
### On Target Nodes
1. Copy the files 'benchmarks.pp', 'apache-php-results.sh', 'mysql-results.sh' and 'fio-results.sh' to all the target nodes
2. Install puppet on each node
3. Apply the standalone manifest to install apache httpd, PHP, MySQL, fio (disk benchmarking utility) and related packages
4. The manifest also installs crons that run each separate benchmark once every hour. Letting them run for 24 hours is a good way to average out random spikes and troughs in system load.

### On your machine
#### (where you aggregate the data from all nodes)
1. Install parallel ssh (pssh on RedHat, parallel-ssh on Ubuntu)
2. Install gnuplot
3. After the waiting period, run the script 'collate-results.sh' locally to gather key results from all the nodes and plot graphs of them using gnuplot
