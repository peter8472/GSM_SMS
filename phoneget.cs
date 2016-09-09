using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;
using System.Threading;

namespace phoneget
{
    
    public class Talker
    {
        public SerialPort port;
        public Talker()
        {
            Thread readThread = new Thread(Read);
            port = new SerialPort("COM3");
            port.Open();
            readThread.Start();
        }
        
        public void Read()
        {
            while (true)
            {
                try
                {
                    string message = port.ReadLine();
                    Console.WriteLine(message);
                } catch (TimeoutException) { }
            }
        }
        public void chat()
        {
            string command, data;
            while (true)
            {
                Console.Write("comamnd> ");
                command = Console.ReadLine();
                port.WriteLine(command + "\r");

            }
        }
    }
    class Program
    {

        static void Main(string[] args)
        {

            string []rayp = System.IO.Ports.SerialPort.GetPortNames();
            
            Console.WriteLine("hello from c#\n");
            Talker talk = new Talker();
            talk.chat();


        }

    }
}
