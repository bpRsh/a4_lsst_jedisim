/* Author    : Bhishan Poudel
 * Date      : Jul 19, 2016
 * Update    : Jun 09, 2017 Fri
 *
 * Compile   : gcc -o jedicolor jedicolor.c -lm -lcfitsio
 * Run       : ./jedicolor color.txt 0.1 0.2
 *
 *
 *
 * Depends   : as from color.txt it combines two fitsfiles into third file
 *             simdatabase/bulge_f8/f814w_bulge0.fits
 *             simdatabase/disk_f8/f814w_disk0.fits
 *             simdatabase/bulge_disk_f8/
 *                                                 
 *
 * Output    : /Users/poudel/jedisim/simdatabase/bulge_disk_f8/bulge_disk_f8_.fits
 *
 * Algorithm : pix3[ii] =   b*pix1[ii] +  d *pix2[ii];
 *
 * Info      : This program reads in two fitsfiles from input directory,
 *             applies the algorithm and create one output fitsfile.
 *
 *             e.g. input  1: simdatabase/bulge_f8/f814w_bulge0.fits
 *                  input  2: simdatabase/disk_f8/f814w_disk0.fits
 *                  output 1: simdatabase/bulge_disk_f8/bdf8_0.fits
 */

#include <stdio.h>
#include <string.h>
#include "fitsio.h"
#define NUM_GALS 201

int main(int argc,char *argv[]){

// variables
int check =1;
int status = 0;
int n=0;
double m;
double m2;
char bulge[NUM_GALS][NUM_GALS];
char disk[NUM_GALS][NUM_GALS];
char bulge_disk[NUM_GALS][NUM_GALS];
char bulge_disk1[NUM_GALS][NUM_GALS];

fitsfile *in1[NUM_GALS]; //fits file for reading red images
fitsfile *in2[NUM_GALS]; //fits file for reading blue images
fitsfile *out[NUM_GALS]; //fitsfile for reading output images

long   anaxes1[3]  = {1,1,1};
long   anaxes2[3]  = {1,1,1};
int    anaxis1     = 0;
int    anaxis2     = 0;
long   npixels     = 1;
long   firstpix[3] = {1,1,1};
long   bitpix      = -32;
int    ii;


// numerical arguments for jedicolor
m  = atof(argv[2]) ;  
m2 = atof(argv[3]) ;  
printf("The factor b =  %f and d = %f\n\n",m,m2);

// input file for jedicolor
FILE *fp;
fp = fopen(argv[1],"r");


//==============================================================================
// note: input file argv[1] e.g. color.txt should have n=NUM_GALS lines
for(n=0;n<NUM_GALS;n++){

    fscanf(fp,"%s %s %s",bulge[n],disk[n],bulge_disk[n]);
    
    // prepend ! sign
    // We run jedicolor as the first program in jedimaster
    // It takes in bulge and disk galaxies and creates bulge_disk galaxies.
    // Then we run jedicatalog and again jedicolor.
    // In second run, it should replace previous outputs.
    // In cfitsio library to replace fitfiles we append ! .
    strcpy(bulge_disk1[n],"!");
    strcat(bulge_disk1[n],bulge_disk[n]);

    // print lines of input file
    //printf("%d: \t%s \t%s \t%s\n",n,bulge[n],disk[n],bulge_disk1[n]);
}
//==============================================================================


// for loop of input file 
for(n=0;n<NUM_GALS;n++){
    fits_open_file(&in1[n],bulge[n],READONLY,&status); // reading blue  files
    //printf("%d %s\n",status,bulge[n]);

    fits_open_file(&in2[n],disk[n],READONLY,&status); //reading red files
    //printf("%d %s\n",status,disk[n]);


    if (status) {
       fits_report_error(stderr, status);
       return(status);
    }

    fits_get_img_dim(in1[n],&anaxis1,&status);
    fits_get_img_dim(in2[n],&anaxis2,&status);
    fits_get_img_size(in1[n],3,anaxes1,&status);
    fits_get_img_size(in1[n],3,anaxes2,&status);

    //printf("%ld %ld\n",anaxes1[0],anaxes2[0]); // no. of pixels in each axis
    //printf("%d\n",anaxis2); // total no. of axis(suppose x,y or z)

    if(check && !fits_create_file(&out[n],bulge_disk1[n],&status)){
        fits_copy_header(in1[n],out[n],&status);

        npixels = anaxes1[0];
        //printf("the value of npixels is %ld\n",npixels);

        double *pix1,*pix2,*pix3;

        pix1 = (double*)malloc(npixels*sizeof(double));
        pix2 = (double*)malloc(npixels*sizeof(double));
        pix3 = (double*)malloc(npixels*sizeof(double));

        if(pix1==NULL|| pix2==NULL){
            printf("Memory allocation error\n");
            return(1);
        }

        //printf("%ld\n",npixels);

        for(firstpix[2]=1;firstpix[2]<=anaxes1[2];firstpix[2]++){
            for(firstpix[1]=1;firstpix[1]<=anaxes1[1];firstpix[1]++){
                if(fits_read_pix(in1[n],TDOUBLE,firstpix,npixels,NULL,pix1,NULL,&status))  break;
                if(fits_read_pix(in2[n],TDOUBLE,firstpix,npixels,NULL,pix2,NULL,&status))  break;

                for(ii=0;ii<npixels;ii++){
                        // pix1[ii] += pix2[ii];
			// m = 1 in jedimaster.py
			// In the loop m is str(i / 20.0) 
                        pix3[ii] = ( m * pix1[ii] ) + ( m2 * pix2[ii]  );
                } //for loop of ii

            fits_update_key(out[n],TLONG,"BITPIX",&bitpix,0,&status);
            fits_write_pix(out[n],TDOUBLE,firstpix,npixels,pix3,&status);

            } //end of for loop of firstpix[2]
        } // end of for loop of firstpix[1]


    free(pix1);
    free(pix2);
    free(pix3);
    fits_close_file(out[n],&status);
    } // end of check

    fits_close_file(in1[n],&status);
    fits_close_file(in2[n],&status);
} // end of for loop of line from input text file

//finally reinitialize the argument m to zero.
m=0;
m2=0;
fclose(fp);
return 0;
} // end of main
