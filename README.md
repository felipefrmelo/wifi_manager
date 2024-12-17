# wifi_manager


# Setting Up `arp-scan` Without `sudo`

To run `arp-scan` without requiring `sudo`, follow these steps:

1. Open a terminal and run the following command to grant the necessary capabilities:

    ```bash
    sudo setcap cap_net_raw,cap_net_admin+eip $(which arp-scan)
    ```

2. Verify the capabilities with:

    ```bash
    getcap $(which arp-scan)
    ```

    You should see output like this:

    ```bash
    /usr/bin/arp-scan = cap_net_raw,cap_net_admin+eip
    ```

3. Test arp-scan without sudo:

   ```bash
   arp-scan -l
   ```

