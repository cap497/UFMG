#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int mem[1024][4] = {0}, cache[64][16][3] = {0};

void printCacheData(){
	printf("\n");
	for(int i=0 ; i<sizeof(cache)/sizeof(*cache) ; i++){
		printf("%d:\t",i);
		for(int j=0 ; j<4*sizeof(**cache[2]) ; j=j+4){
			if(cache[i][j][0] != 0 ) printf(" %d \t",cache[i][j][2]);
			else printf("    -    \t");
		}
		printf("\n");
	}
}

void printCacheTags(){
	printf("\n");
	for(int i=0 ; i<sizeof(cache)/sizeof(*cache) ; i++){
		printf("%d:\t",i);
		for(int j=0 ; j<4*sizeof(**cache[1]) ; j=j+4){
			if(cache[i][j][0] == 0)	printf("-\t");
			else printf("%d\t",cache[i][j][1]);
		}
		printf("\n");
	}
}

void printMem(){
	printf("\n");
	for(int i=0 ; i<sizeof(mem)/sizeof(*mem) ; i++){
		
		if(*mem[i] != 0)
			printf("%d: %d \t",i,*mem[i]);
		else
			printf("%d: \t\t",i);
		if((i+1)%8 == 0) printf("\n");
	}
}

int getLinesNum(char* filename){
	FILE *fp;
	fp = fopen(filename,"r");
	int count=0;
	char c;
	while((c = fgetc(fp)) != EOF){ 
		if(c == '\n') count++;
	}
	count++;
	fclose(fp);
	return count;
}

int getSize(char* filename){
	FILE *fp;
	fp = fopen(filename,"r");
	int count=0;
	char c;
	while((c = fgetc(fp)) != EOF){ 
		if(c == ' ' || c == '\n') count++;
	}
	count++;
	fclose(fp);
	return count;
}

int bin2int(char* str){
	int total = 0;
	while(*str){
		total *= 2;
		if(*str++ == '1') total += 1;
	}
	return total;
}

void str2bin(char* word) { 
    int num = atoi(word); 
    int bin[12];
    
	int i=0;
	while(num>0){
		bin[i] = num%2;
		num = num/2;
		i++;
	}
	
	//printf("%s",word);
	for(int j=i-1 ; j>=0 ; j--){
		printf("%d",bin[j]);
	}
	
	if(strcmp(word,"0")==0) printf("0");
	
	printf(" "); 
}

int main (int argc, char *argv[]){
	int i, count=0, val, index, off, tag;
	float reads=0, writes=0;
	float hits=0, misses=0;
	float hit_rate=0, miss_rate=0;
	char* filename = "CPU.txt";
	
	int size = getSize(filename);
	int lines = getLinesNum(filename);
	
	char *word[size];
	char *out[2*size];
	int j = 0;
	FILE *fp = fopen(filename, "r");
	FILE *res = fopen("result.txt", "w+");
	
	for (i=0 ; i<size ; ++i) {
		word[i] = malloc (32);
		fscanf (fp, "%32s", word[i]);
	}
	
	for (i=0 ; i<size ; ++i){
		//str2bin(word[i]);
		//printf ("%s ", word[i]);
		fprintf (res,"%s ", word[i]);
		if(strcmp(word[i],"0")==0 && count==1){
			reads++;
			
			index = (atoi(word[i-1]) & 252) >> 2;
			off = atoi(word[i-1]) & 3;
			tag = (atoi(word[i-1]) & 768) >> 8;
			
			if(cache[index][4*off][2] != 0){
				hits++;
				//printf("H");
				
				//printf(" %d",cache[index][4*off][2]);
				fprintf(res,"%d ",cache[index][4*off][2]);
				fprintf(res,"H");
			}else{
				misses++;
				//printf("M");
				
				if(*mem[atoi(word[i-1])] != 0){
					fprintf(res,"%d ",*mem[atoi(word[i-1])]);
				}
				fprintf(res,"M");
			}
			count = 0;
			//printf("\t\t\t\t tag=%d\t ind=%d\t off=%d",tag,index,off);
			//printf("\n");
			fprintf(res,"\n");
		}else if(strcmp(word[i],"1")==0 && count==1){
			i++;
			//printf("%s W",word[i]);
			fprintf(res,"%s W",word[i]);
			
			index = (atoi(word[i-2]) & 252) >> 2;
			off = atoi(word[i-2]) & 3;
			tag = (atoi(word[i-2]) & 3840) >> 8;
			//printf("\t tag=%d\t ind=%d\t off=%d",tag,index,off);
			
			if(bin2int(word[i]) != 0){
				if(cache[index][4*off][0] == 0){
					cache[index][4*off][0] = 1;
				}else{
					*mem[atoi(word[i-2])] = cache[index][4*off][2];
				}
				cache[index][4*off][1] = tag;
				cache[index][4*off][2] = bin2int(word[i]);
			}else{
				if(cache[index][4*off][2] == 0){
					*mem[atoi(word[i-2])] = 0;
					cache[index][4*off][1] = 0;
					cache[index][4*off][0] = 0;
				}else{
					cache[index][4*off][2] = 0;
				}
			}
			
			//printf("\n");
			fprintf(res,"\n");
			writes++;
			count = 0;
		}else{
			count++;
		}
	}
	
	hit_rate = hits/reads;
	miss_rate = misses/reads;
	/*
	printf("\nREADS: %.0f\nWRITES: %.0f",reads,writes);
	printf("\nHITS: %.0f\nMISSES: %.0f",hits,misses);
	printf("\nHIT RATE: %f\nMISS RATE: %f\n",hit_rate,miss_rate);
	*/
	fprintf(res,"\nREADS: %.0f\nWRITES: %.0f",reads,writes);
	fprintf(res,"\nHITS: %.0f\nMISSES: %.0f",hits,misses);
	fprintf(res,"\nHIT RATE: %f\nMISS RATE: %f",hit_rate,miss_rate);
	
	//printCacheTags();
	//printCacheData();
	//printMem();
	
	for (i=0 ; i<size ; ++i)
		free (word[i]);
	
    fclose(res);
	fclose(fp); 
	
	return 0;
}
