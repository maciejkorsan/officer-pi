using System;
using System.Configuration;
using System.Linq; 
using System.Net;
using System.Text;
using System.Threading.Tasks; 
using System.IO;
using System.Xml.Serialization;
using Nancy;
using Nancy.ModelBinding;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Microsoft.ServiceBus.Messaging;

namespace SlackAzureServiceBus
{
    public class SlackRequest
    {
        public string Token { get; set; }
        public string Command { get; set; }
        public string Text { get; set; }
        public string Channel_Name { get; set; }
        public string User_Name { get; set; }
    }
 
    
    public class SlackAzureServiceBusModule : NancyModule
    {
        public SlackAzureServiceBusModule() : base("/officer")
        {
            StaticConfiguration.DisableErrorTraces = false;
            Post["/", runAsync: true] = async (_, ct) =>
            {
                var request = this.Bind<SlackRequest>();
                
                if (request.Token != ConfigurationManager.AppSettings["SLACK_SLASH_COMMAND_TOKEN"])
                    return 403;

                if (request.Command != "/officer") return 400;



                var connectionString = ConfigurationManager.AppSettings["SERVICE_BUS_CONNECTION"];
                var queue = QueueClient.CreateFromConnectionString(connectionString, ConfigurationManager.AppSettings["SERVICE_BUS_QUEUE"]);
                
                var payload = Newtonsoft.Json.JsonConvert.SerializeObject(request);

                var payloadStream = new MemoryStream(Encoding.UTF8.GetBytes(payload));
            
                queue.Send(new BrokeredMessage(payloadStream,true));

                return 200;
            };
        }
    }
}