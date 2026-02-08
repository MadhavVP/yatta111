import React from "react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Play, Share2 } from "lucide-react"; // Assuming lucide-react is installed by shadcn or next default

interface LawCardProps {
  title: string;
  summary: string;
  sector: "healthcare" | "education" | "service" | "corporate";
  audioUrl?: string;
  state: string;
}

const LawCard: React.FC<LawCardProps> = ({
  title,
  summary,
  sector,
  audioUrl,
  state,
}) => {
  const getBadgeVariant = (s: string) => {
    switch (s) {
      case "healthcare":
        return "destructive"; // Red for alert
      case "education":
        return "secondary";
      default:
        return "default"; // default is primary (black/slate)
    }
  };

  const playAudio = () => {
    if (audioUrl) {
      new Audio(audioUrl).play();
    } else {
      alert("Audio not available");
    }
  };

  return (
    <Card className="w-full max-w-md shadow-lg border-l-4 border-l-primary/50">
      <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
        <div className="space-y-1">
          <Badge
            variant={getBadgeVariant(sector) as any}
            className="uppercase text-xs font-bold"
          >
            {sector} Alert
          </Badge>
          <span className="text-xs text-muted-foreground ml-2">{state}</span>
        </div>
      </CardHeader>
      <CardContent>
        <CardTitle className="text-lg font-bold mb-2 leading-tight">
          {title}
        </CardTitle>
        <p className="text-sm text-gray-700 leading-relaxed">{summary}</p>
      </CardContent>
      <CardFooter className="flex justify-between pt-2">
        <Button
          variant="outline"
          size="sm"
          onClick={playAudio}
          className="flex gap-2"
        >
          <Play className="h-4 w-4" /> Listen
        </Button>
        <Button size="sm" className="flex gap-2">
          Action
        </Button>
      </CardFooter>
    </Card>
  );
};

export default LawCard;
