import java.io.*;
import java.math.BigInteger;
import java.net.*;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicInteger;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Client {
    
    public static long totalTime;
    
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        System.out.println("Enter a composite number: ");
        BigInteger composite = scan.nextBigInteger();
        
        
        ArrayList<String[]> SERVER_ADDRESSES = new ArrayList<String[]>();
        SERVER_ADDRESSES.add(new String[]{"192.168.56.1", String.valueOf(4000)});
        // SERVER_ADDRESSES.add(new String[]{"127.0.0.2", String.valueOf(4000)});
        
        int workers = 0;
        while (workers < 1 || workers > SERVER_ADDRESSES.size()) {
            System.out.println("Enter the number of workers (1-" + SERVER_ADDRESSES.size() + "): ");
            workers = scan.nextInt();
        }
        
        AtomicInteger CURRENT_MULTIPLE = new AtomicInteger(0);
        for (int i = 0; i < workers; i++) {
            Thread thread = new Thread(new ClientThread(SERVER_ADDRESSES.get(i), composite, CURRENT_MULTIPLE, totalTime));
            thread.start();
        }
        scan.close();
    }
}

class ClientThread implements Runnable {
    private final String serverAddress;
    private final int serverPort;
    private final BigInteger composite;
    private final AtomicInteger currentMultiple;
    private final int chunk_size;
    private long totalTime;

    public ClientThread(String[] serverData, BigInteger composite, AtomicInteger currentMultiple, long totalTime) {
        this.serverAddress = serverData[0];
        this.serverPort = Integer.parseInt(serverData[1]);
        this.composite = composite;
        this.currentMultiple = currentMultiple;
        this.chunk_size = 50000000;
        this.totalTime = totalTime;
    }
    
    @Override
    public void run() {
        try {
            Socket socket = new Socket(serverAddress, serverPort);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            FileWriter fileWriter = new FileWriter("log.txt", true);
            PrintWriter logWriter = new PrintWriter(fileWriter);
            DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
            while (true) {
                try {
                    int multiple = currentMultiple.getAndIncrement();
                    if (composite.compareTo(new BigInteger(String.valueOf(multiple * chunk_size))) == 1) {
                        socket.close();
                        logWriter.close();
                        return;
                    }
                    
                    long start = multiple * chunk_size;
                    if (start == 0) {
                        start = 1;
                    }
                    String str = composite + " " + start + " " + ((multiple + 1) * chunk_size);
                    
                    LocalDateTime now = LocalDateTime.now();  
                    String timestamp = dtf.format(now);

                    String log = String.format("[%s] SENDING, %s, %d, %d, %d", timestamp, serverAddress, composite, multiple * chunk_size, (multiple + 1) * chunk_size);
                    logWriter.println(log);
                    
                    long start_time = System.currentTimeMillis();
                    
                    out.println(str);
                    String response = in.readLine();
                    
                    long time_elapsed = System.currentTimeMillis() - start_time;
                    totalTime += time_elapsed;
                    System.out.println(totalTime);

                    now = LocalDateTime.now();  
                    timestamp = dtf.format(now);

                    // timestamp, send/receiving, remote-addr, composite, lower-bound, upper-bound, return, *time-processed
                    log = String.format("[%s] RECEIVING, %s, %d, %d, %d, %s, %d", timestamp, serverAddress, composite, multiple * chunk_size, (multiple + 1) * chunk_size, response, time_elapsed);
                    logWriter.println(log);
                    
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            // socket.close();
            // logWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}